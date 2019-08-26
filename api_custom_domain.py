import os
import boto3
from asyncio import run, create_task, get_event_loop
from aws_cdk.core import App, Stack
from aws_cdk.aws_apigateway import DomainNameOptions, EndpointType
from aws_cdk.aws_lambda import Function, Runtime, Tracing, Code
from aws_cdk.aws_certificatemanager import DnsValidatedCertificate, ValidationMethod, Certificate
from aws_cdk.aws_route53 import HostedZone

from permissions import ROUTE_53_DNS_ENSURER_POLICY_STATEMENT
from dns_ensurer import DnsEnsurer

class APICustomDomain(Stack):
    def __init__(
            self,
            app: App,
            id: str,
            domain: str,
            sats: list
            ) -> None:

        super().__init__(app, id)
        
    async def setup(self, id: str, domain: str, sats: list) -> None:
        hosted_zone_task = create_task(self.create_hosted_zone(domain=domain))
        potential_cert_arn = await self.get_potential_cert(domain=domain, sats=sats)
        if potential_cert_arn:
            self.cert = Certificate.from_certificate_arn(
                self,
                '{}APICert'.format(id),
                certificate_arn=potential_cert_arn)
            self.create_dno(domain=domain)
            await hosted_zone_task
        else:
            await hosted_zone_task
            self.cert = DnsValidatedCertificate(
                self,
                '{}APICert'.format(id),
                hosted_zone=self.zone,
                domain_name=domain,
                region='us-east-1')
            self.create_dno(domain=domain)
            
    def create_dno(self, domain: str) -> None:
        self.dno = DomainNameOptions(
                    certificate=self.cert,
                    domain_name=domain,
                    endpoint_type=EndpointType.EDGE)

    
    async def get_potential_hosted_zone(self, domain) -> set:
        r53 = boto3.client('route53')
        potential_hosted_zone = list(filter((lambda zone: zone['Name'] == domain), r53.list_hosted_zones()['HostedZones']))
        assert len(potential_hosted_zone) <= 1
        if len(potential_hosted_zone) == 1:
            return potential_hosted_zone[0]
        else:
            return None
        
    async def get_potential_cert(self, domain: str, sats: list) -> set:
        acm = boto3.client('acm', region_name='us-east-1')
        certs = acm.list_certificates(CertificateStatuses=['ISSUED'])[
                    'CertificateSummaryList']
        
        potential_cert_arn = list(filter(lambda cert: cert['DomainName'] == domain, certs))
        assert len(potential_cert_arn) <= 1
        if len(potential_cert_arn) == 1:
            cert_arn = potential_cert_arn[0]['CertificateArn']
            cert = acm.describe_certificate(CertificateArn=cert_arn)
            satsFound = cert['Certificate']['SubjectAlternativeNames']
            if sats == satsFound:
                return cert_arn
        else:
            return None
        
            
    async def create_hosted_zone(self, domain: str) -> HostedZone:
        potential_hosted_zone = await self.get_potential_hosted_zone(domain=domain)
        if potential_hosted_zone:
            self.zone_name = potential_hosted_zone['Name'][:-1]
            if self.zone_name == domain:
                self.hosted_zone_id = potential_hosted_zone['Id'].partition('/hostedzone/')[2]
                print('HostedZone Found:{}\n{}'.format(self.zone_name, self.hosted_zone_id))
                self.zone = HostedZone.from_hosted_zone_attributes(
                    self,
                    '{}HostedZone'.format(id),
                    hosted_zone_id=self.hosted_zone_id,
                    zone_name=self.zone_name)
        else:
            with open('ensure_ns.py', 'r') as content:
                code_txt = content.read()
                self.fod = DnsEnsurer(
                self,
                '{}FOD'.format(id),
                txt=code_txt,
                env={'DOMAIN': domain},
                policies=ROUTE_53_DNS_ENSURER_POLICY_STATEMENT,
                domain=domain)
                self.zone = self.fod.zone
    

