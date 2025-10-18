#!/bin/bash
# Git 워크플로우 자동화 스크립트
# AI-100 프로젝트 규칙 1 준수

set -e  # 에러 발생 시 스크립트 중단

# 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 함수: 로그 출력
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 함수: 현재 브랜치 확인
get_current_branch() {
    git rev-parse --abbrev-ref HEAD
}

# 함수: 변경사항 확인
check_changes() {
    if [[ -z $(git status -s) ]]; then
        log_warn "커밋할 변경사항이 없습니다."
        return 1
    fi
    return 0
}

# 메인 워크플로우
main() {
    log_info "=== Git 워크플로우 시작 ==="

    # 인자 확인
    if [ $# -lt 1 ]; then
        log_error "사용법: $0 <커밋 메시지> [브랜치명]"
        echo "예시: $0 \"[Sprint-001] Python 라이브러리 설치 완료\" feature/python-setup"
        exit 1
    fi

    COMMIT_MESSAGE="$1"
    WORK_BRANCH="${2:-$(get_current_branch)}"
    MAIN_BRANCH="main"

    log_info "작업 브랜치: $WORK_BRANCH"
    log_info "메인 브랜치: $MAIN_BRANCH"
    log_info "커밋 메시지: $COMMIT_MESSAGE"

    # 1. 현재 브랜치 확인 및 전환
    CURRENT_BRANCH=$(get_current_branch)
    if [ "$CURRENT_BRANCH" != "$WORK_BRANCH" ]; then
        log_info "브랜치 전환: $CURRENT_BRANCH -> $WORK_BRANCH"
        git checkout "$WORK_BRANCH" 2>/dev/null || git checkout -b "$WORK_BRANCH"
    fi

    # 2. 변경사항 확인
    if ! check_changes; then
        log_warn "워크플로우를 종료합니다."
        exit 0
    fi

    # 3. 스테이징
    log_info "변경사항 스테이징..."
    git add .

    # 4. 커밋
    log_info "커밋 생성..."
    git commit -m "$COMMIT_MESSAGE"

    # 5. 원격 저장소에 푸시
    log_info "원격 저장소에 푸시: $WORK_BRANCH"
    git push origin "$WORK_BRANCH" || {
        log_warn "업스트림 브랜치 설정 후 푸시..."
        git push -u origin "$WORK_BRANCH"
    }

    # 6. 메인 브랜치로 전환
    log_info "메인 브랜치로 전환: $MAIN_BRANCH"
    git checkout "$MAIN_BRANCH"

    # 7. 메인 브랜치 업데이트
    log_info "메인 브랜치 업데이트..."
    git pull origin "$MAIN_BRANCH" || log_warn "메인 브랜치 pull 실패 (무시하고 계속)"

    # 8. 작업 브랜치 머지
    log_info "작업 브랜치 머지: $WORK_BRANCH -> $MAIN_BRANCH"
    git merge "$WORK_BRANCH" --no-ff -m "Merge $WORK_BRANCH into $MAIN_BRANCH"

    # 9. 메인 브랜치 푸시
    log_info "메인 브랜치 푸시..."
    git push origin "$MAIN_BRANCH"

    # 10. 원래 작업 브랜치로 복귀
    log_info "작업 브랜치로 복귀: $WORK_BRANCH"
    git checkout "$WORK_BRANCH"

    # 11. 작업 브랜치를 메인과 동기화
    log_info "작업 브랜치 동기화..."
    git merge "$MAIN_BRANCH" --no-ff -m "Sync $WORK_BRANCH with $MAIN_BRANCH"

    log_info "=== Git 워크플로우 완료 ==="
    log_info "현재 브랜치: $(get_current_branch)"
    log_info "최근 커밋: $(git log -1 --oneline)"
}

# 스크립트 실행
main "$@"
