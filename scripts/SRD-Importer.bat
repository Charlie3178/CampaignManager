@echo off
echo [*] Starting Arcanryn Database Import Process...
echo -----------------------------------------------

echo [*] Initializing database...
python db_init.py

:: Use the full name pattern to be safe
for %%f in (srd_import_*.py) do (
    echo [>] Running %%f...
    python "%%f"
)

echo -----------------------------------------------
echo [SUCCESS] All SRD imports are complete!
pause