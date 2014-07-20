# config valid only for Capistrano 3.1
lock '3.2.1'

set :application, "bmo_controller"
#set :repository,  "bmo_controller"
set :repo_url, 'git@github.com:perenecabuto/bmo_controller.git'

# Default branch is :master
# ask :branch, proc { `git rev-parse --abbrev-ref HEAD`.chomp }.call

# Default deploy_to directory is /var/www/my_app
# set :deploy_to, '/var/www/my_app'
set :deploy_to, "/opt/apps/bmo_controller"

# Default value for :scm is :git
# set :scm, :git
set :scm, :git
set :repository, "/home/bacamarte/workspace/bmo_controller"

#set :copy_strategy, :export
#set :deploy_via, :copy
set :deploy_via, :capifony_copy_local
set :use_composer,     true
set :use_composer_tmp, true

# Default value for :format is :pretty
set :format, :pretty

# Default value for :log_level is :debug
set :log_level, :debug

# Default value for :pty is false
#set :pty, true

# Default value for :linked_files is []
# set :linked_files, %w{config/database.yml}

# Default value for linked_dirs is []
# set :linked_dirs, %w{bin log tmp/pids tmp/cache tmp/sockets vendor/bundle public/system}

# Default value for default_env is {}
# set :default_env, { path: "/opt/ruby/bin:$PATH" }

# Default value for keep_releases is 5
set :keep_releases, 5


set :user, :deployer
#set :use_sudo, false
set :domain, "caixote"


namespace :log do
  desc "Watch app log"
  task :watch do
    on roles(:app) do
      execute "tail -f /tmp/bmo_daemon.log"
    end
  end
end

namespace :deploy do

  desc 'Restart application'
  task :restart do
    on roles(:app) do
      execute "supervisorctl stop bmo_daemon"
      execute "supervisorctl stop bmo_controller"
      execute "~/virtualenvs/#{fetch :application}/bin/pip install -r #{current_path}/deploy_requirements.txt; true"
      execute "rm -f #{current_path}/bmo_controller.sqlite3 && ln -sf #{shared_path}/bmo_controller.sqlite3 #{current_path}; true"
      execute "supervisorctl start bmo_daemon"
      execute "supervisorctl start bmo_controller"
    end
  end

  after :publishing, :restart

  # this overrides a rails specific thing.
  task :finalize_update do ; end
  task :migrate         do ; end

  task :setup_virtualenv do
    on roles(:app) do
      execute "virtualenv ~/virtualenvs/#{fetch :application}"
    end
  end

  after 'deploy:updated', 'deploy:setup_virtualenv'
  #before 'deploy:start', 'deploy:stop'

  #before 'deploy:restart', 'deploy:stop'
  after 'deploy:finished', 'deploy:restart'
end

def run(ovo)
end
