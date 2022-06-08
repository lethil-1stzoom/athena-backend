from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'hpstore01' # <storage_account_name>
    account_key = 'GWvoTbx15MerKCFEY1AskqoGh+gON75ImyH7DokraXoit6ND2oq+cgErZuosuVD6+qLamjo4UrEzZXVmksNq2w==' # <storage_account_key>
    azure_container = 'media'
    expiration_secs = None
