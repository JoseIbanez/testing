#Install


sudo cp errors.grpc_conf /etc/nginx/conf.d/errors.grpc_conf
sudo cp grpc-site.conf   /etc/nginx/sites-enabled/grpc-site.conf
sudo systemctl reload nginx

sudo systemctl status nginx --no-pager
