import hashlib, json

class MerkleLog:
    def __init__(self):
        self.events = []
    
    def add_event(self, data: dict):
        entry = json.dumps(data, sort_keys=True)
        prev_hash = self.events[-1]["hash"] if self.events else "0"*64
        new_hash = hashlib.sha256((prev_hash + entry).encode()).hexdigest()
        self.events.append({"data": data, "hash": new_hash})
    
    def verify(self):
        prev_hash = "0"*64
        for e in self.events:
            recalculated = hashlib.sha256((prev_hash + json.dumps(e["data"], sort_keys=True)).encode()).hexdigest()
            if recalculated != e["hash"]:
                return False
            prev_hash = e["hash"]
        return True

if __name__ == "__main__":
    log = MerkleLog()
    log.add_event({"user": "anon", "action": "parse"})
    log.add_event({"user": "anon", "action": "rollback"})
    print("Log valid?", log.verify())
    print(log.events)
