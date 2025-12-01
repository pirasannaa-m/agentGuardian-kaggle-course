import hashlib, time, json

class AuditorAgent:
    def __init__(self, kms_signer=None):
        self.kms_signer = kms_signer

    def run(self, report):
        manifest = json.dumps(report, sort_keys=True).encode()
        if self.kms_signer:
            signature = self.kms_signer(manifest)
        else:
            signature = hashlib.sha256(manifest).hexdigest()
        return {'evidence': {'signature': signature, 'timestamp': time.time()}}
