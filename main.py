import json, time

def safe_parser(input_str: str) -> dict:
    """Parser sûr avec validation stricte et schéma minimal JSON"""
    try:
        data = json.loads(input_str)
        if not isinstance(data, dict):
            raise ValueError("Invalid structure")
        return data
    except Exception as e:
        return {"error": str(e)}

class RollbackGuard:
    def __init__(self, max_attempts=3, window=60):
        self.attempts = []
        self.max_attempts = max_attempts
        self.window = window
    
    def allow(self):
        now = time.time()
        self.attempts = [t for t in self.attempts if now - t < self.window]
        if len(self.attempts) >= self.max_attempts:
            return False
        self.attempts.append(now)
        return True

if __name__ == "__main__":
    # Démo parser
    safe = safe_parser('{"hello":"world"}')
    print("Parsed:", safe)

    # Démo rollback guard
    guard = RollbackGuard(max_attempts=2, window=5)
    for i in range(4):
        print("Attempt", i, "allowed?", guard.allow())
        time.sleep(1)
