from fabric.api import *

# NEED TO BE CHANGED!!!!!!!!!!!!!!
env.hosts=["ec2-52-41-107-14.us-west-2.compute.amazonaws.com"]
env.user="ubuntu"
env.key_filename=['/home/yang/Desktop/chatbot.pem']
YOUR_NAME_HERE='Yang'

def test_local():
    print local('ls -a')

def test_remote():
    print run('ls -a')

def setup_ec2():
    with settings(warn_only=True), hide('output'):
        anaconda_downloaded = run('ls Anaconda2-4.3.0-Linux-x86_64.sh')
        anaconda_installed = run('ls /home/ubuntu/anaconda2')
        server_is_at = run('curl icanhazip.com')
        put('myproject.ini')
        put('wsgi.py')
        put(local_path='myproject.service', remote_path='/etc/systemd/system/myproject.service', use_sudo=True)

        with open('myproject', 'r+') as infile:
            contents = infile.read()
            contents = contents.replace('server_domain_or_IP', server_is_at)
            infile.seek(0)
            infile.truncate()
            infile.write(contents)


        with open('myproject.py', 'r+') as infile:
            contents = infile.read()
            infile.seek(0)
            infile.truncate()
            infile.write(contents)
        put('myproject.py')

        if anaconda_installed.failed:
            if anaconda_downloaded.failed:
                run('wget https://repo.continuum.io/archive/Anaconda2-4.3.0-Linux-x86_64.sh')
                anaconda_downloaded.succeeded = True

            print '\n\n INSTALLING ANACONDA 2.7; THIS WILL TAKE A WHILE'
            run('bash Anaconda2-4.3.0-Linux-x86_64.sh -b')

        if anaconda_downloaded.succeeded:
            run('rm Anaconda2-4.3.0-Linux-x86_64.sh')

        conda_in_bashrc = run('cat .bashrc | grep anaconda2')
        if conda_in_bashrc.failed:
            run("""echo 'export PATH="/home/ubuntu/anaconda2/bin:$PATH"' >> .bashrc """)

        conda_in_profile = run('cat .profile | grep anaconda2')
        if conda_in_profile.failed:
            run("""echo 'export PATH="/home/ubuntu/anaconda2/bin:$PATH"' >> .profile """)


        sudo('apt-get update')
        sudo('apt-get install -y build-essential python-dev nginx')


        chatbot_env = run('conda env list | grep chatbot')
        if chatbot_env.failed:
            print '\n\nCREATING A SEPARATE ENVIRONMENT FOR THE CHATBOT. THIS WILL TAKE A MINUTE OR TWO.'
            run('conda create -y --name chatbot python=2 anaconda')


        put(local_path='myproject', remote_path='/etc/nginx/sites-available/myproject', use_sudo=True)
        sudo('ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled')

        service_installed = sudo('service myproject status | grep "myproject.service - uWSGI instance to serve myproject"')
        nginx_config_present = sudo('ls /etc/nginx/sites-available/myproject')

        with prefix('source activate chatbot'):
            in_chatbot = run('which pip | grep chatbot')
            if in_chatbot:
                run('pip install flask uwsgi')
                if service_installed.succeeded:
                    print '\n\nuWSGI service installed!'
                if nginx_config_present.succeeded:
                    print '\n\nnginx config is present!'
            else:
                print '\n\nTHERE WAS A PROBLEM WITH THE CHATBOT ENV'

        sudo('service myproject restart')
        sudo('systemctl daemon-reload')
        sudo('service nginx restart')
        print '\n\n\n\n\n\n\n\n OPEN THIS ADDRESS IN YOUR BROWSER: {}:41953\n\n\n\n'.format(server_is_at)

        # Need to test uwsgi --socket 0.0.0.0:8000 --protocol=http -w wsgi
