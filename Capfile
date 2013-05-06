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
  desc "Restart Application"
  task :restart, :roles => :app do
    run "workon #{application}"
    run "pip install -r #{current_path}/deploy_requirements.txt"
    run "cd #{current_path} && gunicorn wsgi -c gunicorn.conf"
  end
end

namespace :log do
  desc "Watch app log"
  task :watch, :roles => :app do
    run "tail -f #{current_path}/log/thin.log"
  end
end
