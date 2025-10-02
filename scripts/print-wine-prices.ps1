$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)

$uri = 'http://127.0.0.1:8080/api/wines/vinos'

try {
    $json = Invoke-RestMethod -Uri $uri -Method GET
} catch {
    Write-Error ("Failed to fetch {0}: {1}" -f $uri, $_)
    exit 1
}

if (-not $json) {
    Write-Host 'No data returned.'
    exit 0
}

$rows = foreach ($w in $json) {
    $pairs = @()
    if ($w.prices) {
        $keys = ($w.prices | Get-Member -MemberType NoteProperty | Select-Object -ExpandProperty Name) | Sort-Object
        foreach ($k in $keys) {
            $v = $w.prices.$k
            if ($null -ne $v -and $v -ne '') { $pairs += ("$k=$v") }
        }
    }
    [PSCustomObject]@{
        id     = $w.id
        name   = $w.name
        prices = ($pairs -join '; ')
    }
}

$sorted = $rows | Sort-Object id
$table = $sorted | Format-Table -AutoSize | Out-String -Width 8192

# Write to console and also save to files for review
Write-Host $table
$outDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$sorted | Export-Csv -NoTypeInformation -Encoding UTF8 -Path (Join-Path $outDir 'wine-prices.csv')
$table | Set-Content -Encoding UTF8 -Path (Join-Path $outDir 'wine-prices.txt')
Write-Host ("Saved: {0}" -f (Join-Path $outDir 'wine-prices.csv'))
Write-Host ("Saved: {0}" -f (Join-Path $outDir 'wine-prices.txt'))