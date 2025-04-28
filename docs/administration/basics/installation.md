# Quick installation guide

To start using GenFlow, you first need to install it. This guide provides installation instructions
for the most commonly used operating systems.
If your operating system is not listed, you should be able to adapt the steps provided to suit your system.

If you are behind a proxy server, additional configuration may be required. Please note that this
guide does not cover proxy setup, as it is an advanced topic.

## Ubuntu 24.04 (x86_64/amd64)

- Update the package index and install required dependencies:

  ```shell
  sudo apt update
  sudo apt install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common
  ```

- Type commands below to install Docker. More
  instructions can be found [here](https://docs.docker.com/install/linux/docker-ce/ubuntu/).

  ```shell
  sudo install -m 0755 -d /etc/apt/keyrings
  sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
  sudo chmod a+r /etc/apt/keyrings/docker.asc
  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  sudo apt-get update
  sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  ```

- To run Docker without sudo, add your user to the docker group:

  ```shell
  sudo usermod -aG docker $USER
  ```

  Log out and log back in to apply the group changes. You can type `groups` command in a terminal
  window after that and check if `docker` group is in its output.

- Check if Docker is installed correctly and works without `sudo`:

  ```shell
  docker run hello-world
  ```

  You should see a message confirming that Docker is installed and running correctly.

- To access GenFlow over a network or through a different system, export `GF_HOST` environment variable

  ```shell
  export GF_HOST=FQDN_or_YOUR-IP-ADDRESS
  ```

- Create new folder in your home directory, and create new file with the installation commands:

  ```shell
  mkdir ~/genflow
  cd ~/genflow
  echo \
    "
    " > ~/genflow/install.sh
  chmod u+x ~/genflow/install.sh
  ~/genflow/install.sh
  ```

- Create a super user to use the admin panel:

  ```shell
  docker exec -it genflow_server bash -ic 'python3 ~/manage.py createsuperuser'
  ```

  Choose a username and a password for your admin account. For more information
  please read [Django documentation](https://docs.djangoproject.com/en/2.2/ref/django-admin/#createsuperuser).

- Open your browser and go to [localhost:8080](http://localhost:8080). Now you should be able to
register new users and login to GenFlow.

- To access the admin panel go to [Admin Panel](http://localhost:8080/admin)
