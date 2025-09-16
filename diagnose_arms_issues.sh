#!/bin/bash
# ARMS监控问题诊断和修复脚本
# 用于诊断和修复ARMS监控相关问题

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查ARMS探针安装
check_arms_probe() {
    log_info "检查ARMS探针安装状态..."
    
    # 检查aliyun-bootstrap是否安装
    if ! command -v aliyun-bootstrap &> /dev/null; then
        log_error "aliyun-bootstrap未安装"
        return 1
    fi
    
    # 检查探针是否安装
    if ! python -c "import aliyun.opentelemetry" 2>/dev/null; then
        log_error "ARMS探针未安装"
        log_info "正在安装ARMS探针..."
        aliyun-bootstrap -a install
        if [[ $? -eq 0 ]]; then
            log_success "ARMS探针安装成功"
        else
            log_error "ARMS探针安装失败"
            return 1
        fi
    else
        log_success "ARMS探针已安装"
    fi
    
    # 检查aliyun-instrument命令
    if ! command -v aliyun-instrument &> /dev/null; then
        log_error "aliyun-instrument命令不可用"
        return 1
    else
        log_success "aliyun-instrument命令可用"
    fi
}

# 检查环境变量
check_environment_variables() {
    log_info "检查ARMS环境变量..."
    
    local required_vars=(
        "ARMS_APP_NAME"
        "ARMS_REGION_ID"
        "ARMS_LICENSE_KEY"
        "ARMS_IS_PUBLIC"
        "ARMS_ENDPOINT"
    )
    
    local missing_vars=()
    
    for var in "${required_vars[@]}"; do
        if [[ -z "${!var}" ]]; then
            missing_vars+=("$var")
        fi
    done
    
    if [[ ${#missing_vars[@]} -gt 0 ]]; then
        log_warning "缺少环境变量: ${missing_vars[*]}"
        log_info "设置环境变量..."
        
        export ARMS_APP_NAME="campus_market"
        export ARMS_REGION_ID="cn-hangzhou"
        export ARMS_LICENSE_KEY="biimgsqhcm@6ca181feeeac0da"
        export ARMS_IS_PUBLIC="True"
        export ARMS_ENDPOINT="https://arms-dc-hz.aliyuncs.com"
        
        log_success "环境变量设置完成"
    else
        log_success "ARMS环境变量配置正确"
    fi
}

# 检查网络连接
check_network_connectivity() {
    log_info "检查网络连接..."
    
    # 检查ARMS端点连接
    if curl -k -s --connect-timeout 10 "$ARMS_ENDPOINT" > /dev/null; then
        log_success "ARMS端点连接正常"
    else
        log_error "无法连接到ARMS端点: $ARMS_ENDPOINT"
        return 1
    fi
    
    # 检查DNS解析
    if nslookup arms-dc-hz.aliyuncs.com > /dev/null 2>&1; then
        log_success "DNS解析正常"
    else
        log_warning "DNS解析可能有问题"
    fi
}

# 检查应用状态
check_application_status() {
    log_info "检查应用状态..."
    
    # 检查应用进程
    if pgrep -f "gunicorn.*wsgi:app" > /dev/null; then
        log_success "应用进程运行中"
        
        # 获取进程信息
        local pid=$(pgrep -f "gunicorn.*wsgi:app" | head -1)
        log_info "应用PID: $pid"
        
        # 检查进程是否使用aliyun-instrument启动
        if ps aux | grep $pid | grep -q "aliyun-instrument"; then
            log_success "应用使用ARMS探针启动"
        else
            log_warning "应用未使用ARMS探针启动"
            return 1
        fi
    else
        log_error "应用进程未运行"
        return 1
    fi
    
    # 检查端口监听
    if netstat -tlnp 2>/dev/null | grep -q ":80 "; then
        log_success "端口80监听正常"
    else
        log_error "端口80未监听"
        return 1
    fi
}

# 检查日志文件
check_logs() {
    log_info "检查日志文件..."
    
    local log_file="logs/gunicorn_service.log"
    
    if [[ -f "$log_file" ]]; then
        log_success "日志文件存在: $log_file"
        
        # 检查ARMS探针启动日志
        if grep -q "Aliyun python agent is started" "$log_file"; then
            log_success "ARMS探针启动日志存在"
        else
            log_warning "ARMS探针启动日志不存在"
        fi
        
        # 检查错误日志
        if grep -q "ERROR\|Exception\|Traceback" "$log_file"; then
            log_warning "发现错误日志"
            echo "最近的错误日志:"
            grep -A 5 -B 5 "ERROR\|Exception\|Traceback" "$log_file" | tail -20
        else
            log_success "未发现错误日志"
        fi
    else
        log_error "日志文件不存在: $log_file"
        return 1
    fi
}

# 生成测试流量
generate_test_traffic() {
    log_info "生成测试流量..."
    
    if [[ -f "test_arms_monitoring.py" ]]; then
        log_info "运行ARMS监控测试..."
        python test_arms_monitoring.py
        log_success "测试流量生成完成"
    else
        log_warning "测试脚本不存在，手动生成测试流量..."
        
        # 简单的curl测试
        for i in {1..10}; do
            curl -s "http://localhost:80/" > /dev/null
            curl -s "http://localhost:80/api/categories" > /dev/null
            sleep 1
        done
        
        log_success "手动测试流量生成完成"
    fi
}

# 修复ARMS问题
fix_arms_issues() {
    log_info "开始修复ARMS问题..."
    
    # 停止现有应用
    log_info "停止现有应用..."
    if pgrep -f "gunicorn.*wsgi:app" > /dev/null; then
        pkill -f "gunicorn.*wsgi:app"
        sleep 3
        log_success "现有应用已停止"
    fi
    
    # 设置环境变量
    check_environment_variables
    
    # 启动应用
    log_info "使用ARMS探针重新启动应用..."
    cd /root/campus_market
    
    # 激活conda环境
    source $(conda info --base)/etc/profile.d/conda.sh
    conda activate condavenv
    
    # 使用aliyun-instrument启动
    nohup aliyun-instrument \
        --service_name="campus_market" \
        --traces_exporter=otlp \
        --metrics_exporter=otlp \
        --logs_exporter=otlp \
        --exporter_otlp_endpoint="$ARMS_ENDPOINT" \
        --exporter_otlp_headers="Authentication=$ARMS_LICENSE_KEY" \
        --resource_attributes="service.name=campus_market,service.version=1.0.0" \
        gunicorn --config gunicorn.conf.py wsgi:app \
        > logs/gunicorn_service.log 2>&1 &
    
    local app_pid=$!
    echo $app_pid > logs/app.pid
    
    # 等待应用启动
    sleep 5
    
    if ps -p $app_pid > /dev/null; then
        log_success "应用重新启动成功 (PID: $app_pid)"
    else
        log_error "应用重新启动失败"
        return 1
    fi
}

# 生成诊断报告
generate_diagnosis_report() {
    log_info "生成诊断报告..."
    
    local report_file="logs/arms_diagnosis_report_$(date +%Y%m%d_%H%M%S).txt"
    
    {
        echo "ARMS监控诊断报告"
        echo "=================="
        echo "诊断时间: $(date)"
        echo ""
        
        echo "1. 系统信息:"
        echo "   操作系统: $(uname -a)"
        echo "   Python版本: $(python --version)"
        echo "   当前用户: $(whoami)"
        echo "   工作目录: $(pwd)"
        echo ""
        
        echo "2. ARMS探针状态:"
        if python -c "import aliyun.opentelemetry" 2>/dev/null; then
            echo "   探针状态: 已安装"
        else
            echo "   探针状态: 未安装"
        fi
        
        if command -v aliyun-instrument &> /dev/null; then
            echo "   aliyun-instrument: 可用"
        else
            echo "   aliyun-instrument: 不可用"
        fi
        echo ""
        
        echo "3. 环境变量:"
        echo "   ARMS_APP_NAME: ${ARMS_APP_NAME:-未设置}"
        echo "   ARMS_REGION_ID: ${ARMS_REGION_ID:-未设置}"
        echo "   ARMS_LICENSE_KEY: ${ARMS_LICENSE_KEY:-未设置}"
        echo "   ARMS_ENDPOINT: ${ARMS_ENDPOINT:-未设置}"
        echo ""
        
        echo "4. 应用状态:"
        if pgrep -f "gunicorn.*wsgi:app" > /dev/null; then
            echo "   应用状态: 运行中"
            local pid=$(pgrep -f "gunicorn.*wsgi:app" | head -1)
            echo "   应用PID: $pid"
            
            if ps aux | grep $pid | grep -q "aliyun-instrument"; then
                echo "   ARMS探针: 已启用"
            else
                echo "   ARMS探针: 未启用"
            fi
        else
            echo "   应用状态: 未运行"
        fi
        echo ""
        
        echo "5. 网络连接:"
        if curl -s --connect-timeout 5 "$ARMS_ENDPOINT" > /dev/null 2>&1; then
            echo "   ARMS端点连接: 正常"
        else
            echo "   ARMS端点连接: 异常"
        fi
        echo ""
        
        echo "6. 端口监听:"
        netstat -tlnp 2>/dev/null | grep ":80 " || echo "   端口80: 未监听"
        echo ""
        
        echo "7. 最近日志:"
        if [[ -f "logs/gunicorn_service.log" ]]; then
            echo "   日志文件: logs/gunicorn_service.log"
            echo "   最近日志:"
            tail -10 logs/gunicorn_service.log | sed 's/^/     /'
        else
            echo "   日志文件: 不存在"
        fi
        
    } > "$report_file"
    
    log_success "诊断报告已生成: $report_file"
    echo ""
    cat "$report_file"
}

# 主函数
main() {
    echo "🔍 ARMS监控问题诊断和修复工具"
    echo "================================"
    echo ""
    
    case "${1:-diagnose}" in
        "diagnose")
            log_info "开始诊断ARMS问题..."
            check_arms_probe
            check_environment_variables
            check_network_connectivity
            check_application_status
            check_logs
            generate_diagnosis_report
            ;;
        "fix")
            log_info "开始修复ARMS问题..."
            fix_arms_issues
            generate_test_traffic
            log_success "修复完成，请等待5-10分钟查看ARMS控制台"
            ;;
        "test")
            log_info "生成测试流量..."
            generate_test_traffic
            ;;
        "report")
            generate_diagnosis_report
            ;;
        *)
            echo "用法: $0 {diagnose|fix|test|report}"
            echo ""
            echo "命令说明:"
            echo "  diagnose - 诊断ARMS问题"
            echo "  fix      - 修复ARMS问题"
            echo "  test     - 生成测试流量"
            echo "  report   - 生成诊断报告"
            ;;
    esac
}

# 脚本入口
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
