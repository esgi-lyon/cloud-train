#!/usr/bin/env bash

az deployment group create \
  --name ExampleDeployment \
  --resource-group "$1" \
  --template-file arm.template.json \
  --parameters extensions_enablevmaccess_username=azure \
    extensions_enablevmaccess_ssh_key="$(cat ~/.ssh/id_rsa.pub)" \
    extensions_enablevmaccess_reset_ssh=true \
    extensions_enablevmaccess_expiration=100000 \
    extensions_enablevmaccess_remove_user=null
