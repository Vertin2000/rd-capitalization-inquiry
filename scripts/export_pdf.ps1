# Export final_slides.pptx to final_slides.pdf via PowerPoint COM
$ErrorActionPreference = "Stop"
$pptxPath = (Resolve-Path "outputs/final_slides.pptx").Path
$pdfPath  = (Join-Path (Get-Location).Path "final_slides.pdf")
Write-Host "Source: $pptxPath"
Write-Host "Target: $pdfPath"
$ppt = New-Object -ComObject PowerPoint.Application
try {
    $pres = $ppt.Presentations.Open($pptxPath, $true, $false, $false)
    $pres.SaveAs($pdfPath, 32)  # 32 = ppSaveAsPDF
    $pres.Close()
    Write-Host "PDF exported OK"
} finally {
    $ppt.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppt) | Out-Null
}
