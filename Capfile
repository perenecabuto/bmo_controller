# encoding: utf-8

load 'deploy'

set :application, "bmo_controller"
set :repository,  "bmo_controller"

set :scm, :git
set :repository, "."

set :copy_strategy, :export
set :deploy_via, :copy

ssh_options[:forward_agent] = true

set :stage, :production
set :user, :deployer
set :use_sudo, false
set :deploy_to, "/opt/apps/#{application}"
set :domain, "caixote"

role :web, domain
role :app, domain

namespace :deploy do
  task :start do
    run "~/virtualenvs/#{application}/bin/pip install -r #{current_path}/deploy_requirements.txt"
    run "rm #{current_path}/bmo_controller.sqlite3 && ln -sf #{shared_path}/bmo_controller.sqlite3 #{current_path}"
    run "cd #{current_path} && DJANGO_SETTINGS_MODULE=settings ~/virtualenvs/#{application}/bin/gunicorn wsgi -c gunicorn.conf"
  end

  task :stop do
    run "killall -9 gunicorn > /dev/null 2>&1 &"
  end

  # this overrides a rails specific thing.
  task :finalize_update do ; end
  task :migrate         do ; end

  task :setup_virtualenv do
    run "virtualenv ~/virtualenvs/#{application}"
  end

  after 'deploy:setup', 'deploy:setup_virtualenv'

  before 'deploy:start', 'deploy:stop'
  after 'deploy:start', 'bmo_daemon:start'

  after 'deploy:stop', 'bmo_daemon:stop'

  before 'deploy:restart', 'deploy:stop'
  after 'deploy:restart', 'deploy:start'
end

namespace :bmo_daemon do
    task :start do
        run "cd #{current_path} && PYTHONPATH=$PYTHONPATH:. DJANGO_SETTINGS_MODULE=settings nohup ~/virtualenvs/#{application}/bin/django-admin.py bmo_daemon >/dev/null 2>&1 &"
    end

    task :stop do
        run "ps awx | grep 'bmo_daemo[n]' | cut -d' ' -f1 | xargs kill -9"
    end

    before 'bmo_daemon:start', 'bmo_daemon:stop'
    after 'deploy:start', 'bmo_daemon:start'
end

namespace :log do
  desc "Watch app log"
  task :watch, :roles => :app do
    run "tail -f #{current_path}/log/thin.log"
  end
end
