export APP_VERSION='0.01'
export SITE_DOMAIN='guyandjaella.com'
export STATIC_DOMAIN="d3fqzsbh169wiu.cloudfront.net"
export TEMPLATE_URI="dashboard.html"
export SITE_CERT="arn:aws:acm:us-east-1:936272581790:certificate/831328ac-9045-470c-9bf4-1ed45be52bb3"
export SITE_HOSTED_ZONE_ID="ZACA05K52IZCC"
export APP_VERSION="0.01"
export DEV="True"

alias gstat='git status'
alias gpush='git push origin master'
alias gfet='git fetch'
alias deploy='cdk deploy --require-approval never'
alias test='pytest site_function/test*py'