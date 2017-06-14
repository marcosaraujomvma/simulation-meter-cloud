openssl genrsa -out key.pem
yes '' | openssl req -new -x509 -key key.pem -out crt.pem -days 36500 || exit 1
cat key.pem crt.pem > cert.pem
rm key.pem crt.pem

fingerprint=`openssl x509 -in cert.pem -md5 -fingerprint -noout | sed 's/^[^=]\+=//;s/://g' | tr 'A-Z' 'a-z'`

echo -e "\n\nfingerprint=$fingerprint"
