sudo cp /srv/www/django/2020-1-CECD3-Generator-8/aws_files/uwsgi.service /etc/systemd/system/uwsgi.service
sudo cp /srv/www/django/2020-1-CECD3-Generator-8/aws_files/uwsgi.ini /srv/www/django/ini/uwsgi.ini
sudo cp /srv/www/django/2020-1-CECD3-Generator-8/aws_files/default /etc/nginx/sites-available/default

sudo systemctl daemon-reload
sudo systemctl restart uwsgi nginx
