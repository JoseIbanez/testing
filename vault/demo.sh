export VAULT_ADDR="http://127.0.0.1:8200"


ubuntu@m1:~$ vault init
Unseal Key 1: c83vuccFZ1ev2IL4tb2pmSBnZf9BLfjw4IiYzo0Jq0s+
Unseal Key 2: FjyaO+UBrZwX0hvkv8RYhn2KDfzznj6h4jieGkVFRVv/
Unseal Key 3: 3sDipd0cNM6ylprQ6fdkLORgetaqstUicbitGmz8s/fQ
Unseal Key 4: +ozbcl8X9QwF/DG+CsgYcdnHEshZ4NfG/VjOu2+Piu29
Unseal Key 5: pswa4yOPZbZUi+rSVUpJmIYMS0YBW98r9MRAmapUt0Cr
Initial Root Token: 468ffcd9-7353-21bc-93e6-3cc72a306da7

Vault initialized with 5 keys and a key threshold of 3. Please
securely distribute the above keys. When the vault is re-sealed,
restarted, or stopped, you must provide at least 3 of these keys
to unseal it again.

Vault does not store the master key. Without at least 3 keys,
your vault will remain permanently sealed.


vault unseal 

vault audit-enable file file_path=/var/log/vault_audit.log


#token 
root token: 3cbc700f-da08-9383-eb10-df45e1cb3b13
vault auth 3cbc700f-da08-9383-eb10-df45e1cb3b13

#github
vault auth-enable github
vault auth -methods

vault write auth/github/config organization=vault-2018
vault write auth/github/map/teams/dev value=dev-policy
vault write auth/github/map/teams/fls value=fls-policy
vault write auth/github/map/teams/sls value=sls-policy

github my token: c409dc1dfa119937ea8aa871e772b67ab1bab1bd
vault auth -method=github token=c409dc1dfa119937ea8aa871e772b67ab1bab1bd


#userpass
vault auth-enable userpass
vault write auth/userpass/users/jibanezw \
    password=foo \
    policies=policy-02-sls

vault list auth/userpass/users
vault read auth/userpass/users/jibanezw


vault auth -method=userpass \
    username=jibanezw \
    password=foo

#policy
vault policy-write policy-01-fls policy-01-fls.hcl
vault policy-write policy-02-sls policy-02-sls.hcl
vault policies





