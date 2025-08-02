import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.models.guild_member import GuildMember
from src.schemas.guild_member import GuildMemberCreate


class TestHealthAPI:
    """健康检查API测试"""
    
    def test_health_check(self, client: TestClient):
        """测试健康检查端点"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data


class TestMembersAPI:
    """成员API测试"""
    
    def test_get_members_empty(self, client: TestClient, db_session: Session):
        """测试获取空成员列表"""
        response = client.get("/api/members")
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0
        assert data["page"] == 1
        assert data["size"] == 10
    
    def test_create_member(self, client: TestClient, db_session: Session, sample_guild_member_data):
        """测试创建成员"""
        response = client.post("/api/members", json=sample_guild_member_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_guild_member_data["name"]
        assert data["class_name"] == sample_guild_member_data["class_name"]
        assert "id" in data
    
    def test_get_members_with_data(self, client: TestClient, db_session: Session, sample_guild_members_data):
        """测试获取有数据的成员列表"""
        # 创建测试数据
        for member_data in sample_guild_members_data:
            client.post("/api/members", json=member_data)
        
        response = client.get("/api/members")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 3
        assert data["total"] == 3
    
    def test_get_member_by_id(self, client: TestClient, db_session: Session, sample_guild_member_data):
        """测试根据ID获取成员"""
        # 创建成员
        create_response = client.post("/api/members", json=sample_guild_member_data)
        member_id = create_response.json()["id"]
        
        # 获取成员
        response = client.get(f"/api/members/{member_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == sample_guild_member_data["name"]
    
    def test_get_member_not_found(self, client: TestClient, db_session: Session):
        """测试获取不存在的成员"""
        response = client.get("/api/members/999")
        assert response.status_code == 404
    
    def test_update_member(self, client: TestClient, db_session: Session, sample_guild_member_data):
        """测试更新成员"""
        # 创建成员
        create_response = client.post("/api/members", json=sample_guild_member_data)
        member_id = create_response.json()["id"]
        
        # 更新成员
        update_data = {"name": "更新后的名字", "level": 71}
        response = client.put(f"/api/members/{member_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "更新后的名字"
        assert data["level"] == 71
    
    def test_delete_member(self, client: TestClient, db_session: Session, sample_guild_member_data):
        """测试删除成员"""
        # 创建成员
        create_response = client.post("/api/members", json=sample_guild_member_data)
        member_id = create_response.json()["id"]
        
        # 删除成员
        response = client.delete(f"/api/members/{member_id}")
        assert response.status_code == 204
        
        # 验证成员已被删除
        get_response = client.get(f"/api/members/{member_id}")
        assert get_response.status_code == 404
    
    def test_search_members(self, client: TestClient, db_session: Session, sample_guild_members_data):
        """测试搜索成员"""
        # 创建测试数据
        for member_data in sample_guild_members_data:
            client.post("/api/members", json=member_data)
        
        # 搜索战士
        response = client.get("/api/members?search=战士")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["name"] == "战士玩家"
    
    def test_filter_by_class(self, client: TestClient, db_session: Session, sample_guild_members_data):
        """测试按职业筛选"""
        # 创建测试数据
        for member_data in sample_guild_members_data:
            client.post("/api/members", json=member_data)
        
        # 筛选法师
        response = client.get("/api/members?class_name=法师")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["class_name"] == "法师"
    
    def test_pagination(self, client: TestClient, db_session: Session, sample_guild_members_data):
        """测试分页"""
        # 创建测试数据
        for member_data in sample_guild_members_data:
            client.post("/api/members", json=member_data)
        
        # 测试第一页
        response = client.get("/api/members?page=1&size=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["page"] == 1
        assert data["size"] == 2
        assert data["total"] == 3


class TestStatisticsAPI:
    """统计API测试"""
    
    def test_get_overview_statistics(self, client: TestClient, db_session: Session, sample_guild_members_data):
        """测试获取总览统计"""
        # 创建测试数据
        for member_data in sample_guild_members_data:
            client.post("/api/members", json=member_data)
        
        response = client.get("/api/statistics/overview")
        assert response.status_code == 200
        data = response.json()
        assert data["total_members"] == 3
        assert data["online_members"] == 2
        assert data["offline_members"] == 1
    
    def test_get_class_distribution(self, client: TestClient, db_session: Session, sample_guild_members_data):
        """测试获取职业分布"""
        # 创建测试数据
        for member_data in sample_guild_members_data:
            client.post("/api/members", json=member_data)
        
        response = client.get("/api/statistics/class-distribution")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        # 验证职业分布
        class_names = [item["class_name"] for item in data]
        assert "战士" in class_names
        assert "法师" in class_names
        assert "猎人" in class_names
    
    def test_get_faction_distribution(self, client: TestClient, db_session: Session, sample_guild_members_data):
        """测试获取阵营分布"""
        # 创建测试数据
        for member_data in sample_guild_members_data:
            client.post("/api/members", json=member_data)
        
        response = client.get("/api/statistics/faction-distribution")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["faction"] == "联盟"
        assert data[0]["count"] == 3


class TestCrawlerAPI:
    """爬虫API测试"""
    
    def test_get_crawler_status(self, client: TestClient):
        """测试获取爬虫状态"""
        response = client.get("/api/crawler/status")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "last_run" in data
    
    def test_get_guild_info(self, client: TestClient):
        """测试获取公会信息"""
        response = client.get("/api/crawler/guild-info")
        assert response.status_code == 200
        data = response.json()
        assert "guild_name" in data
        assert "realm" in data
    
    def test_test_api_connection(self, client: TestClient):
        """测试API连接"""
        response = client.post("/api/crawler/test-api")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data


class TestErrorHandling:
    """错误处理测试"""
    
    def test_invalid_member_data(self, client: TestClient, db_session: Session):
        """测试无效的成员数据"""
        invalid_data = {
            "name": "",  # 空名字
            "level": 999  # 无效等级
        }
        response = client.post("/api/members", json=invalid_data)
        assert response.status_code == 422
    
    def test_invalid_pagination(self, client: TestClient, db_session: Session):
        """测试无效的分页参数"""
        response = client.get("/api/members?page=-1&size=0")
        assert response.status_code == 422
    
    def test_method_not_allowed(self, client: TestClient):
        """测试不允许的HTTP方法"""
        response = client.patch("/api/members/1")
        assert response.status_code == 405 