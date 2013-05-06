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
  task :start do ; end
  task :stop do ; end

  # this overrides a rails specific thing.
  task :finalize_update do ; end
  task :migrate         do ; end

  desc "Restart Application"
  task :restart, :roles => :app do
    run ". ~/virtualenvs/#{application}/bin/activate && pip install -r #{current_path}/deploy_requirements.txt"
    run "cd #{current_path} && ~/virtualenvs/#{application}/bin/gunicorn wsgi -c gunicorn.conf"
  end

  task :setup_virtualenv do
    run "virtualenv ~/virtualenvs/#{application}"
  end

  after 'deploy:setup', 'deploy:setup_virtualenv'
end

namespace :log do
  desc "Watch app log"
  task :watch, :roles => :app do
    run "tail -f #{current_path}/log/thin.log"
  end
end
