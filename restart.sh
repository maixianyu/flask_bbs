#!/usr/bin/env bash

# 不要在 sites-available 里面放任何东西
cp /var/www/flask_bbs/flask_bbs.nginx /etc/nginx/sites-enabled/flask_bbs
chmod -R o+rwx /var/www/flask_bbs

cp /var/www/flask_bbs/flask_bbs.conf /etc/supervisor/conf.d/flask_bbs.conf


# 初始化
cd /var/www/flask_bbs


# 重启服务器
service supervisor restart
service nginx restart

echo 'succsss'
echo 'ip'
hostname -I
