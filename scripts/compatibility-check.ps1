# 호환성 및 에러 체크 스크립트 (PowerShell)
# AI-100 프로젝트 규칙 2 준수

param(
    [Parameter(Mandatory=$false)]
    [string]$CheckType = "full"  # full, quick, python, nodejs
)

$ErrorActionPreference = "Stop"

# 색상 함수
function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Green
}

function Write-Warn {
    param([string]$Message)
    Write-Host "[WARN] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Write-Success {
    param([string]$Message)
    Write-Host "[✓] $Message" -ForegroundColor Green
}

function Write-Fail {
    param([string]$Message)
    Write-Host "[✗] $Message" -ForegroundColor Red
}

# 체크 결과 저장
$script:CheckResults = @{
    TotalChecks = 0
    PassedChecks = 0
    FailedChecks = 0
    Warnings = 0
    Errors = @()
}

# Python 환경 체크
function Test-PythonEnvironment {
    Write-Info "=== Python 환경 체크 ==="
    $script:CheckResults.TotalChecks++

    try {
        # Python 버전 확인
        $pythonVersion = python --version 2>&1
        Write-Success "Python 설치 확인: $pythonVersion"

        # pip 확인
        $pipVersion = pip --version 2>&1
        Write-Success "pip 설치 확인: $pipVersion"

        # requirements.txt 확인
        if (Test-Path "requirements.txt") {
            Write-Success "requirements.txt 존재 확인"

            # 설치된 패키지 확인
            Write-Info "주요 패키지 설치 확인..."
            $packages = @("pandas", "numpy", "scikit-learn", "torch", "transformers", "streamlit", "fastapi")

            foreach ($pkg in $packages) {
                try {
                    python -c "import $pkg" 2>$null
                    Write-Success "  - $pkg 설치 확인"
                } catch {
                    Write-Warn "  - $pkg 미설치 또는 오류"
                    $script:CheckResults.Warnings++
                }
            }
        } else {
            Write-Warn "requirements.txt 파일이 없습니다."
            $script:CheckResults.Warnings++
        }

        $script:CheckResults.PassedChecks++
        return $true
    } catch {
        Write-Fail "Python 환경 체크 실패: $_"
        $script:CheckResults.FailedChecks++
        $script:CheckResults.Errors += "Python: $_"
        return $false
    }
}

# Node.js 환경 체크
function Test-NodeEnvironment {
    Write-Info "=== Node.js 환경 체크 ==="
    $script:CheckResults.TotalChecks++

    try {
        # Node 버전 확인
        $nodeVersion = node --version 2>&1
        Write-Success "Node.js 설치 확인: $nodeVersion"

        # npm 확인
        $npmVersion = npm --version 2>&1
        Write-Success "npm 설치 확인: $npmVersion"

        # package.json 확인
        if (Test-Path "package.json") {
            Write-Success "package.json 존재 확인"

            # node_modules 확인
            if (Test-Path "node_modules") {
                Write-Success "node_modules 폴더 존재 확인"

                # package-lock.json 확인
                if (Test-Path "package-lock.json") {
                    Write-Success "package-lock.json 존재 확인"
                } else {
                    Write-Warn "package-lock.json이 없습니다."
                    $script:CheckResults.Warnings++
                }
            } else {
                Write-Warn "node_modules 폴더가 없습니다. 'npm install' 실행 필요"
                $script:CheckResults.Warnings++
            }
        } else {
            Write-Warn "package.json 파일이 없습니다."
            $script:CheckResults.Warnings++
        }

        $script:CheckResults.PassedChecks++
        return $true
    } catch {
        Write-Fail "Node.js 환경 체크 실패: $_"
        $script:CheckResults.FailedChecks++
        $script:CheckResults.Errors += "Node.js: $_"
        return $false
    }
}

# 파일 구조 체크
function Test-FileStructure {
    Write-Info "=== 파일 구조 체크 ==="
    $script:CheckResults.TotalChecks++

    $requiredFiles = @(
        ".claude/rules.md",
        "README.md",
        "QUICK_START.md"
    )

    $requiredDirs = @(
        "docs",
        "docs/sprints",
        "docs/tasks",
        "docs/phases",
        "docs/logs",
        "scripts"
    )

    $allGood = $true

    foreach ($file in $requiredFiles) {
        if (Test-Path $file) {
            Write-Success "파일 존재: $file"
        } else {
            Write-Warn "파일 없음: $file"
            $script:CheckResults.Warnings++
            $allGood = $false
        }
    }

    foreach ($dir in $requiredDirs) {
        if (Test-Path $dir) {
            Write-Success "폴더 존재: $dir"
        } else {
            Write-Warn "폴더 없음: $dir"
            $script:CheckResults.Warnings++
            $allGood = $false
        }
    }

    if ($allGood) {
        $script:CheckResults.PassedChecks++
        return $true
    } else {
        return $false
    }
}

# Git 상태 체크
function Test-GitStatus {
    Write-Info "=== Git 상태 체크 ==="
    $script:CheckResults.TotalChecks++

    try {
        # Git 저장소 확인
        git rev-parse --git-dir 2>$null | Out-Null
        Write-Success "Git 저장소 확인"

        # 현재 브랜치
        $branch = git rev-parse --abbrev-ref HEAD
        Write-Info "현재 브랜치: $branch"

        # 변경사항 확인
        $status = git status -s
        if ([string]::IsNullOrWhiteSpace($status)) {
            Write-Success "커밋되지 않은 변경사항 없음"
        } else {
            Write-Warn "커밋되지 않은 변경사항 존재"
            Write-Host $status
            $script:CheckResults.Warnings++
        }

        $script:CheckResults.PassedChecks++
        return $true
    } catch {
        Write-Fail "Git 상태 체크 실패: $_"
        $script:CheckResults.FailedChecks++
        $script:CheckResults.Errors += "Git: $_"
        return $false
    }
}

# 환경 변수 체크
function Test-EnvironmentVariables {
    Write-Info "=== 환경 변수 체크 ==="
    $script:CheckResults.TotalChecks++

    if (Test-Path ".env") {
        Write-Success ".env 파일 존재"
        $script:CheckResults.PassedChecks++
        return $true
    } elseif (Test-Path ".env.example") {
        Write-Warn ".env 파일 없음 (.env.example만 존재)"
        Write-Info "다음 명령어로 .env 파일 생성: cp .env.example .env"
        $script:CheckResults.Warnings++
        return $false
    } else {
        Write-Warn ".env 및 .env.example 파일 없음"
        $script:CheckResults.Warnings++
        return $false
    }
}

# 종합 호환성 체크
function Test-Compatibility {
    Write-Info "=== 호환성 종합 체크 시작 ==="
    Write-Host ""

    # 체크 타입에 따라 실행
    switch ($CheckType) {
        "python" {
            Test-PythonEnvironment
        }
        "nodejs" {
            Test-NodeEnvironment
        }
        "quick" {
            Test-FileStructure
            Test-GitStatus
        }
        "full" {
            Test-PythonEnvironment
            Test-NodeEnvironment
            Test-FileStructure
            Test-GitStatus
            Test-EnvironmentVariables
        }
    }

    Write-Host ""
    Write-Info "=== 체크 결과 요약 ==="
    Write-Host "총 체크 항목: $($script:CheckResults.TotalChecks)"
    Write-Host "통과: $($script:CheckResults.PassedChecks)" -ForegroundColor Green
    Write-Host "실패: $($script:CheckResults.FailedChecks)" -ForegroundColor Red
    Write-Host "경고: $($script:CheckResults.Warnings)" -ForegroundColor Yellow

    if ($script:CheckResults.FailedChecks -eq 0 -and $script:CheckResults.Warnings -eq 0) {
        Write-Host ""
        Write-Success "✅ 모든 체크 통과!"
        return $true
    } elseif ($script:CheckResults.FailedChecks -eq 0) {
        Write-Host ""
        Write-Warn "⚠️ 경고 항목이 있습니다. 확인이 필요합니다."
        return $true
    } else {
        Write-Host ""
        Write-Fail "❌ 실패한 체크가 있습니다."
        Write-Host ""
        Write-Host "오류 목록:" -ForegroundColor Red
        foreach ($error in $script:CheckResults.Errors) {
            Write-Host "  - $error" -ForegroundColor Red
        }
        return $false
    }
}

# 체크 결과를 파일로 저장
function Save-CheckReport {
    $timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
    $reportDir = "docs/logs/$(Get-Date -Format 'yyyy-MM-dd')"

    if (-not (Test-Path $reportDir)) {
        New-Item -ItemType Directory -Path $reportDir -Force | Out-Null
    }

    $reportPath = "$reportDir/compatibility-check-$timestamp.md"

    $report = @"
# 호환성 체크 보고서

**생성 시간**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
**체크 타입**: $CheckType

## 결과 요약

- 총 체크 항목: $($script:CheckResults.TotalChecks)
- 통과: $($script:CheckResults.PassedChecks)
- 실패: $($script:CheckResults.FailedChecks)
- 경고: $($script:CheckResults.Warnings)

## 상태

$(if ($script:CheckResults.FailedChecks -eq 0 -and $script:CheckResults.Warnings -eq 0) {
    "✅ 모든 체크 통과"
} elseif ($script:CheckResults.FailedChecks -eq 0) {
    "⚠️ 경고 항목 존재"
} else {
    "❌ 실패한 체크 존재"
})

## 오류 목록

$(if ($script:CheckResults.Errors.Count -gt 0) {
    $script:CheckResults.Errors | ForEach-Object { "- $_" } | Out-String
} else {
    "없음"
})

---

**보고서 생성**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
"@

    $report | Out-File -FilePath $reportPath -Encoding UTF8
    Write-Info "체크 보고서 저장: $reportPath"
}

# 메인 실행
try {
    $result = Test-Compatibility
    Save-CheckReport

    if ($result) {
        exit 0
    } else {
        exit 1
    }
} catch {
    Write-Error "체크 스크립트 실행 중 오류: $_"
    exit 1
}
