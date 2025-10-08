$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$reportDir = "report\$timestamp"

# Run pytest with html report in timestamped folder
pytest --html="$reportDir\report.html" --self-contained-html -v
