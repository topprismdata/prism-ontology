# -*- coding: utf-8 -*-
"""
generate_full_profile_registry.py
=================================
基于谋圣 152 列数据映射实际引用的 105 个唯一 URI，
为 prism-ontology/profiles/outlet-insight/ 自动化生成 100% 闭包的 Profile 规范文件：
- concepts.yaml
- relations.yaml
- metric-definitions.yaml (包含全量 78 个业务指标与结构指标)
- sources.yaml (7 个外部数据源)
- organizations.yaml (组织实体)
"""
import yaml
from pathlib import Path

PROFILE_DIR = Path(__file__).resolve().parent.parent / "profiles" / "outlet-insight"
MAP_PATH = Path("/Users/ghb/sh-store-insight/skill/references/dataset_mapping.yaml")

with open(MAP_PATH, "r", encoding="utf-8") as f:
    map_data = yaml.safe_load(f)

# 1. 提取所有 metric URIs
metric_entries = []
# 先加入结构化分析指标
metric_entries.extend([
    {
        "uri": "prism:metric/HerfindahlHirschmanIndex",
        "name": "赫芬达尔-赫希曼指数 (HHI)",
        "category": "Structure",
        "formula": "HHI = sum((s_i * 100)^2)",
        "numerator": "特定品牌在指定区域业态下的网点数",
        "denominator": "区域业态全部网点数",
        "eligible_population": "全部在册品牌",
        "interpretation_boundary": "网点物理覆盖集中度，非实际销售金额市场份额"
    },
    {
        "uri": "prism:metric/Top4ConcentrationRatio",
        "name": "行业前四集中率 (CR4)",
        "category": "Structure",
        "formula": "CR4 = sum(s_1..s_4)",
        "numerator": "排名前4位品牌网点数之和",
        "denominator": "区域业态网点总数",
        "eligible_population": "全部在册品牌",
        "interpretation_boundary": "用于描述头部聚集度（>0.65 为高集中）"
    },
    {
        "uri": "prism:metric/Top8ConcentrationRatio",
        "name": "行业前八集中率 (CR8)",
        "category": "Structure",
        "formula": "CR8 = sum(s_1..s_8)",
        "numerator": "排名前8位品牌网点数之和",
        "denominator": "区域业态网点总数",
        "eligible_population": "全部在册品牌",
        "interpretation_boundary": "用于描述头部集中度"
    },
    {
        "uri": "prism:metric/GiniCoefficient",
        "name": "基尼系数 (Gini)",
        "category": "Structure",
        "formula": "Gini = (2 * sum(i * y_i) - (n + 1) * sum(y_i)) / (n * sum(y_i))",
        "numerator": "网点规模偏斜累积和",
        "denominator": "均等分布基准",
        "eligible_population": "各商圈/大区",
        "interpretation_boundary": "衡量网点在空间或品牌维度的分布不均衡程度"
    }
])

for entry in map_data["mappings"]:
    sp = entry.get("semantic_pattern") or {}
    metric_uri = sp.get("observed_property") or sp.get("estimated_property")
    if metric_uri and metric_uri.startswith("prism:metric/"):
        name = entry.get("physical_column") or metric_uri.split("/")[-1]
        category = "DerivedEstimate" if entry.get("field_class") == "derived_estimate" else "Observation"
        metric_entries.append({
            "uri": metric_uri,
            "name": name,
            "category": category,
            "physical_column": entry.get("physical_column"),
            "data_source": sp.get("data_source"),
            "channel_applicability": sp.get("channel_applicability", "all"),
            "eligible_population": "全部在册售点" if category == "Observation" else "符合模型特征要求的网点",
            "interpretation_boundary": f"源自字段「{entry.get('physical_column')}」的客观测量或模型估计"
        })

with open(PROFILE_DIR / "metric-definitions.yaml", "w", encoding="utf-8") as f:
    yaml.dump({"version": "1.0.0", "profile": "prism://ontology/profiles/outlet-insight", "metrics": metric_entries}, f, allow_unicode=True, sort_keys=False)

# 2. 生成 concepts.yaml (全量 22 个受管 Class)
concepts = [
    {"uri": "prism:core/Entity", "name": "客观实体", "category": "Core"},
    {"uri": "prism:core/DerivedEstimate", "name": "派生推导估计", "category": "Core"},
    {"uri": "prism:core/InformationObject", "name": "信息对象", "category": "Core"},
    {"uri": "prism:core/Observation", "name": "客观观测", "category": "Core"},
    {"uri": "prism:core/Role", "name": "业务角色", "category": "Core"},
    {"uri": "prism:core/Activity", "name": "业务活动", "category": "Core"},
    {"uri": "prism:core/SpatialGeometry", "name": "空间几何与区域", "category": "Core"},
    {"uri": "prism:core/Evidence", "name": "数据证据", "category": "Core"},
    {"uri": "prism:outlet/Outlet", "name": "商业售点", "category": "Outlet"},
    {"uri": "prism:outlet/Brand", "name": "商业品牌/集团", "category": "Outlet"},
    {"uri": "prism:outlet/CommercialSite", "name": "商业场所/商圈", "category": "Outlet"},
    {"uri": "prism:outlet/AdministrativeRegion", "name": "行政区划区域", "category": "Outlet"},
    {"uri": "prism:outlet/Territory", "name": "销售责任辖区", "category": "Outlet"},
    {"uri": "prism:outlet/ChannelType", "name": "业态渠道分类", "category": "Outlet"},
    {"uri": "prism:outlet/OutletObservation", "name": "售点客观观测", "category": "Outlet"},
    {"uri": "prism:outlet/DemographicObservation", "name": "人口客流画像观测", "category": "Outlet"},
    {"uri": "prism:outlet/AssetAndDisplayObservation", "name": "店内设备陈列观测", "category": "Outlet"},
    {"uri": "prism:outlet/TownshipContext", "name": "下沉乡镇市场上下文", "category": "Outlet"},
    {"uri": "prism:outlet/CompetitorSalesVolume", "name": "竞品销量观测(物理缺失)", "category": "Outlet"},
    {"uri": "prism:quality/EntityResolutionAssessment", "name": "实体解析与匹配评估", "category": "Quality"},
    {"uri": "prism:quality/MatchPairAssessment", "name": "匹配对质量评估", "category": "Quality"},
    {"uri": "prism:provenance/DataEngineeringContext", "name": "数据工程上下文", "category": "Provenance"},
    {"uri": "prism:sales/CustomerAccount", "name": "企业客户账户", "category": "Sales"},
    {"uri": "prism:sales/CustomerRole", "name": "客户业务角色", "category": "Sales"},
    {"uri": "prism:sales/ServiceRelationship", "name": "销售服务关系", "category": "Sales"},
    {"uri": "prism:insight/AnalysisIntent", "name": "业务分析意图", "category": "Insight"},
    {"uri": "prism:insight/MetricDefinition", "name": "受管度量定义", "category": "Insight"},
    {"uri": "prism:insight/ComputationActivity", "name": "确定性分析活动", "category": "Insight"},
    {"uri": "prism:insight/InsightClaim", "name": "分析主张", "category": "Insight"},
    {"uri": "prism:insight/QualityAssessment", "name": "数据质量与适用性评估", "category": "Insight"},
    {"uri": "prism:insight/InsightPackage", "name": "标准洞察包", "category": "Insight"},
    {"uri": "prism:insight/ElevationCandidate", "name": "提升事实候选物", "category": "Insight"}
]

with open(PROFILE_DIR / "concepts.yaml", "w", encoding="utf-8") as f:
    yaml.dump({"version": "1.0.0", "profile": "prism://ontology/profiles/outlet-insight", "concepts": concepts}, f, allow_unicode=True, sort_keys=False)

# 3. 生成 relations.yaml (全量受管属性与关系)
relations = [
    {"uri": "prism:core/hasIdentifier", "name": "持有标识", "domain": "prism:core/Entity"},
    {"uri": "prism:core/hasName", "name": "名称", "domain": "prism:core/Entity"},
    {"uri": "prism:core/hasPhysicalAddress", "name": "物理地址", "domain": "prism:core/Entity"},
    {"uri": "prism:core/playsRole", "name": "承担角色", "domain": "prism:core/Entity", "range": "prism:core/Role"},
    {"uri": "prism:core/observesEntity", "name": "观测对象", "domain": "prism:core/Observation", "range": "prism:core/Entity"},
    {"uri": "prism:core/derivedFrom", "name": "派生自", "domain": "prism:core/DerivedEstimate"},
    {"uri": "prism:outlet/locatedInAdministrativeRegion", "name": "位于行政区", "domain": "prism:outlet/Outlet", "range": "prism:outlet/AdministrativeRegion"},
    {"uri": "prism:outlet/coveredBySalesTerritory", "name": "属于销售辖区", "domain": "prism:outlet/Outlet", "range": "prism:outlet/Territory"},
    {"uri": "prism:outlet/territoryCoversRegion", "name": "辖区覆盖行政区", "domain": "prism:outlet/Territory", "range": "prism:outlet/AdministrativeRegion"},
    {"uri": "prism:outlet/belongsToBrand", "name": "归属品牌", "domain": "prism:outlet/Outlet", "range": "prism:outlet/Brand"},
    {"uri": "prism:outlet/operatedAtSite", "name": "经营场所", "domain": "prism:outlet/Outlet", "range": "prism:outlet/CommercialSite"},
    {"uri": "prism:outlet/hasChannelType", "name": "具备业态分类", "domain": "prism:outlet/Outlet", "range": "prism:outlet/ChannelType"},
    {"uri": "prism:outlet/observesOutlet", "name": "观测网点", "domain": "prism:outlet/OutletObservation", "range": "prism:outlet/Outlet"},
    {"uri": "prism:lifecycle/EntityOnlineTime", "name": "网点上线时间", "domain": "prism:outlet/Outlet"},
    {"uri": "prism:lifecycle/RecordCreationTime", "name": "账户建档时间", "domain": "prism:sales/CustomerAccount"},
    {"uri": "prism:sales/accountRepresentsOutlet", "name": "账户代表售点", "domain": "prism:sales/CustomerAccount", "range": "prism:outlet/Outlet"},
    {"uri": "prism:sales/accountRealizesRole", "name": "账户实现角色", "domain": "prism:sales/CustomerAccount", "range": "prism:sales/CustomerRole"},
    {"uri": "prism:sales/outletPlaysCustomerRole", "name": "售点承担客户角色", "domain": "prism:outlet/Outlet", "range": "prism:sales/CustomerRole"},
    {"uri": "prism:insight/hasClaim", "name": "包含主张", "domain": "prism:insight/InsightPackage", "range": "prism:insight/InsightClaim"},
    {"uri": "prism:insight/groundedInEvidence", "name": "基于数据证据", "domain": "prism:insight/InsightClaim", "range": "prism:core/Evidence"}
]

with open(PROFILE_DIR / "relations.yaml", "w", encoding="utf-8") as f:
    yaml.dump({"version": "1.0.0", "profile": "prism://ontology/profiles/outlet-insight", "relations": relations}, f, allow_unicode=True, sort_keys=False)

# 4. 生成 sources.yaml
sources = [
    {"uri": "prism:source/Ctrip", "name": "携程酒店/民宿平台", "category": "ExternalOnlineTravelAgency"},
    {"uri": "prism:source/Dianping", "name": "大众点评本地生活平台", "category": "ExternalLocalLifeService"},
    {"uri": "prism:source/AMap", "name": "高德地图/扫街状元榜", "category": "ExternalLocationService"},
    {"uri": "prism:source/LocationIntelligence", "name": "移动信令商圈人口客流大数据", "category": "TelecomLocationIntelligence"},
    {"uri": "prism:source/FieldExecutionAudit", "name": "太古业务员实地店内审计", "category": "FieldAudit"},
    {"uri": "prism:source/GeocodingAuditService", "name": "腾讯POI坐标与地址解析质检服务", "category": "DataQualityService"},
    {"uri": "prism:source/SwireTownshipMaster", "name": "太古下沉乡镇主数据中心", "category": "EnterpriseMasterData"}
]

with open(PROFILE_DIR / "sources.yaml", "w", encoding="utf-8") as f:
    yaml.dump({"version": "1.0.0", "profile": "prism://ontology/profiles/outlet-insight", "sources": sources}, f, allow_unicode=True, sort_keys=False)

# 5. 生成 organizations.yaml
orgs = [
    {"uri": "prism:org/SwireCocaCola", "name": "太古可口可乐装瓶集团", "category": "EnterpriseBottler", "role": "ServiceRelationshipSubject"}
]

with open(PROFILE_DIR / "organizations.yaml", "w", encoding="utf-8") as f:
    yaml.dump({"version": "1.0.0", "profile": "prism://ontology/profiles/outlet-insight", "organizations": orgs}, f, allow_unicode=True, sort_keys=False)

print("Successfully generated full profile registry in", PROFILE_DIR)
