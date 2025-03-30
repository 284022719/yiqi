<#
.SYNOPSIS
生成目录树形结构并保存到文本文件

.DESCRIPTION
此脚本会递归扫描指定目录，生成带缩进和类型标记的树形结构，
并保存到指定的文本文件中。

.PARAMETER rootPath
要扫描的根目录路径（默认为脚本所在目录）

.PARAMETER outputFile
输出文件路径（默认为脚本所在目录下的FileTree_Structured.txt）

.EXAMPLE
.\FileTreeGenerator.ps1
生成当前目录的结构

.EXAMPLE
.\FileTreeGenerator.ps1 -rootPath "C:\Projects" -outputFile "C:\temp\project_tree.txt"
生成指定目录的结构并保存到指定位置
#>

param (
    [string]$rootPath = $PSScriptRoot,
    [string]$outputFile = "$PSScriptRoot\FileTree_Structured.txt"
)

# 检查目录是否存在
if (-not (Test-Path -Path $rootPath -PathType Container)) {
    Write-Host "错误：目录不存在 - $rootPath" -ForegroundColor Red
    exit 1
}

# 生成带缩进的树形结构
try {
    $results = Get-ChildItem -Path $rootPath -Recurse -ErrorAction Stop | ForEach-Object {
        $fullPathParts = $_.FullName.Split([System.IO.Path]::DirectorySeparatorChar)
        $rootPathParts = $rootPath.Split([System.IO.Path]::DirectorySeparatorChar)
        $depth = $fullPathParts.Count - $rootPathParts.Count
        $indent = '    ' * $depth
        $type = if ($_.PSIsContainer) { "[DIR] " } else { "[FILE]" }
        $size = if (!$_.PSIsContainer) { " ($([math]::Round($_.Length/1KB, 2)) KB)" } else { "" }
        
        "$indent├─ $type $($_.Name)$size"
    }
    
    $results | Out-File -FilePath $outputFile -Encoding UTF8
    Write-Host "成功生成文件结构到: $outputFile" -ForegroundColor Green
}
catch {
    Write-Host "发生错误: $_" -ForegroundColor Red
    exit 1
}