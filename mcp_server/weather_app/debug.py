import traceback
import sys

print("STEP 1: starting import test", file=sys.stderr)

try:
    print("STEP 2: importing mongo_tools", file=sys.stderr)
    from weather_app.app.tools.mongo import mongo_tools
    print("STEP 3: mongo_tools imported OK", file=sys.stderr)

except Exception as e:
    print("❌ IMPORT FAILED", file=sys.stderr)
    traceback.print_exc()
    sys.exit(1)

print("✅ DONE", file=sys.stderr)
