# Convert DOCX to PDF using Word
Add-Type -AssemblyName Microsoft.Office.Interop.Word
$word = New-Object -ComObject Word.Application
$word.Visible = $false

try {
    # Open the document
    $doc = $word.Documents.Open((Resolve-Path 'reports\Robert_Reichert_Resume_20251026_171243.docx').Path)
    
    # Export as PDF
    $pdfPath = 'reports\Robert_Reichert_Resume_20251026_171243.pdf'
    $doc.SaveAs([ref]$pdfPath, [ref]17)  # 17 = PDF format
    
    # Close and cleanup
    $doc.Close()
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
    
    Write-Host "PDF created successfully: $pdfPath"
} catch {
    Write-Host "Error: $_"
} finally {
    if ($word) {
        $word.Quit()
    }
}
