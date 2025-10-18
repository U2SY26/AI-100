# Git 워크플로우 자동화 스크립트 (PowerShell)
# AI-100 프로젝트 규칙 1 준수

param(
    [Parameter(Mandatory=$true)]
    [string]$CommitMessage,

    [Parameter(Mandatory=$false)]
    [string]$WorkBranch = ""
)

# 에러 발생 시 중단
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

# 현재 브랜치 가져오기
function Get-CurrentBranch {
    return git rev-parse --abbrev-ref HEAD
}

# 변경사항 확인
function Test-Changes {
    $status = git status -s
    if ([string]::IsNullOrWhiteSpace($status)) {
        Write-Warn "커밋할 변경사항이 없습니다."
        return $false
    }
    return $true
}

# 메인 워크플로우
function Start-GitWorkflow {
    Write-Info "=== Git 워크플로우 시작 ==="

    # 작업 브랜치 설정
    if ([string]::IsNullOrWhiteSpace($WorkBranch)) {
        $WorkBranch = Get-CurrentBranch
    }

    $MainBranch = "main"

    Write-Info "작업 브랜치: $WorkBranch"
    Write-Info "메인 브랜치: $MainBranch"
    Write-Info "커밋 메시지: $CommitMessage"

    # 1. 현재 브랜치 확인 및 전환
    $CurrentBranch = Get-CurrentBranch
    if ($CurrentBranch -ne $WorkBranch) {
        Write-Info "브랜치 전환: $CurrentBranch -> $WorkBranch"
        try {
            git checkout $WorkBranch 2>$null
        } catch {
            git checkout -b $WorkBranch
        }
    }

    # 2. 변경사항 확인
    if (-not (Test-Changes)) {
        Write-Warn "워크플로우를 종료합니다."
        return
    }

    # 3. 스테이징
    Write-Info "변경사항 스테이징..."
    git add .

    # 4. 커밋
    Write-Info "커밋 생성..."
    git commit -m $CommitMessage

    # 5. 원격 저장소에 푸시
    Write-Info "원격 저장소에 푸시: $WorkBranch"
    try {
        git push origin $WorkBranch
    } catch {
        Write-Warn "업스트림 브랜치 설정 후 푸시..."
        git push -u origin $WorkBranch
    }

    # 6. 메인 브랜치로 전환
    Write-Info "메인 브랜치로 전환: $MainBranch"
    git checkout $MainBranch

    # 7. 메인 브랜치 업데이트
    Write-Info "메인 브랜치 업데이트..."
    try {
        git pull origin $MainBranch
    } catch {
        Write-Warn "메인 브랜치 pull 실패 (무시하고 계속)"
    }

    # 8. 작업 브랜치 머지
    Write-Info "작업 브랜치 머지: $WorkBranch -> $MainBranch"
    git merge $WorkBranch --no-ff -m "Merge $WorkBranch into $MainBranch"

    # 9. 메인 브랜치 푸시
    Write-Info "메인 브랜치 푸시..."
    git push origin $MainBranch

    # 10. 원래 작업 브랜치로 복귀
    Write-Info "작업 브랜치로 복귀: $WorkBranch"
    git checkout $WorkBranch

    # 11. 작업 브랜치를 메인과 동기화
    Write-Info "작업 브랜치 동기화..."
    git merge $MainBranch --no-ff -m "Sync $WorkBranch with $MainBranch"

    Write-Info "=== Git 워크플로우 완료 ==="
    Write-Info "현재 브랜치: $(Get-CurrentBranch)"
    $lastCommit = git log -1 --oneline
    Write-Info "최근 커밋: $lastCommit"
}

# 스크립트 실행
try {
    Start-GitWorkflow
} catch {
    Write-Error "워크플로우 실행 중 오류 발생: $_"
    exit 1
}
