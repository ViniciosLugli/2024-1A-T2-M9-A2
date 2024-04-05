class ConfigVault:
    BOOTSTRAP_SERVERS = 'localhost:29092'
    CLIENT_ID = 'python-producer'
    GROUP_ID = 'python-consumer-group'
    AUTO_OFFSET_RESET = 'earliest'

    @staticmethod
    def producer_config():
        return {
            'bootstrap.servers': ConfigVault.BOOTSTRAP_SERVERS,
            'client.id': ConfigVault.CLIENT_ID
        }

    @staticmethod
    def consumer_config():
        return {
            'bootstrap.servers': ConfigVault.BOOTSTRAP_SERVERS,
            'group.id': ConfigVault.GROUP_ID,
            'auto.offset.reset': ConfigVault.AUTO_OFFSET_RESET
        }

    @staticmethod
    def mongo_uri():
        return 'mongodb://localhost:27017'
