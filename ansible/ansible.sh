#!/bin/bash

DELAY = 1

while [[ $REPLY != 0 ]]; do
    clear
    cat << EOF
        1. Create AWS arhitecture
        2. Configure Ec2 servers
        3. Exit the program
EOF
    
read -p "Enter the right input"
 if [[ $REPLY =~ ^[0-2]$ ]]; then 

    if [[ $REPLY == 1 ]];then 
        echo "aws"
   #     ansible-playbook site.yml -- tags "aws"
    fi
    if [[ $REPLY == 2 ]];then 
        echo "ec2"
    #    ansible-playbook site.yml -- tags "config"
    fi

fi


done

echo "Ansible script closed"
