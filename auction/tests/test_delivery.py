"""Merged delivery tests: QA levels, schema validation, and per-category schemas.

Combines test_deliverable_qa.py and test_delivery_schemas_e2e.py into three sections.
"""

import random
import time

import pytest

from auction.deliverable_qa import QAResult, check_delivery, get_qa_level, validate_delivery_schema
from auction.delivery_schemas import (
    AERIAL_LIDAR_SCHEMA,
    AERIAL_PHOTO_SCHEMA,
    AERIAL_THERMAL_SCHEMA,
    BRIDGE_INSPECTION_SCHEMA,
    CONFINED_SCHEMA,
    CORRIDOR_SCHEMA,
    ENV_SENSING_SCHEMA,
    GROUND_DELIVERY_SCHEMA,
    GROUND_GPR_SCHEMA,
    GROUND_LIDAR_SCHEMA,
    get_delivery_schema,
)

# ════════════════════════════════════════════════════════════════════
# Section 1: QA Level Tests
# ════════════════════════════════════════════════════════════════════


class TestQALevelSelection:
    def test_explicit_override(self):
        spec = {"capability_requirements": {"qa_level": 0}, "task_category": "site_survey"}
        assert get_qa_level(spec) == 0

    def test_env_sensing_defaults_to_1(self):
        assert get_qa_level({"task_category": "env_sensing"}) == 1

    def test_site_survey_defaults_to_2(self):
        assert get_qa_level({"task_category": "site_survey"}) == 2

    def test_unknown_category_defaults_to_1(self):
        assert get_qa_level({"task_category": "unknown_thing"}) == 1

    def test_clamp_to_range(self):
        spec = {"capability_requirements": {"qa_level": 99}}
        assert get_qa_level(spec) == 3
        spec2 = {"capability_requirements": {"qa_level": -5}}
        assert get_qa_level(spec2) == 0


class TestLevel0:
    def test_always_passes(self):
        result = check_delivery({}, {}, qa_level=0)
        assert result.status == "PASS"
        assert result.level == 0

    def test_level_0_empty_data_passes(self):
        result = check_delivery({}, {}, qa_level=0)
        assert result.status == "PASS"


class TestLevel1:
    def test_basic_valid_delivery(self):
        data = {"temperature_c": 22.5, "humidity_pct": 45.0}
        spec = {
            "task_category": "env_sensing",
            "capability_requirements": {
                "qa_level": 1,
                "payload": {"format": "json", "fields": ["temperature_c", "humidity_pct"]},
            },
        }
        result = check_delivery(data, spec)
        assert result.status == "PASS"
        assert result.level == 1

    def test_missing_required_field_fails(self):
        data = {"temperature_c": 22.5}
        spec = {
            "capability_requirements": {
                "qa_level": 1,
                "payload": {"fields": ["temperature_c", "humidity_pct"]},
            },
        }
        result = check_delivery(data, spec)
        assert result.status == "FAIL"
        assert any("humidity_pct" in i for i in result.issues)

    def test_empty_data_fails(self):
        result = check_delivery({}, {"capability_requirements": {"qa_level": 1}})
        assert result.status == "FAIL"

    def test_readings_array_valid(self):
        data = {
            "readings": [
                {"waypoint": 1, "temperature_c": 22.4, "humidity_pct": 45.2},
                {"waypoint": 2, "temperature_c": 23.1, "humidity_pct": 43.8},
            ],
            "summary": "All good",
        }
        spec = {"capability_requirements": {"qa_level": 1, "payload": {"fields": ["readings"]}}}
        result = check_delivery(data, spec)
        assert result.status == "PASS"

    def test_temperature_out_of_range_warns(self):
        data = {"temperature_c": 200.0}
        spec = {"capability_requirements": {"qa_level": 1}}
        result = check_delivery(data, spec)
        assert result.status == "WARN"
        assert any("plausible range" in i for i in result.issues)

    def test_readings_plausibility(self):
        data = {"readings": [{"temperature_c": -50}]}
        spec = {"capability_requirements": {"qa_level": 1}}
        result = check_delivery(data, spec)
        assert any("plausible range" in i for i in result.issues)


class TestLevel2:
    def test_passes_with_all_standards_data(self):
        data = {
            "readings": [{"temperature_c": 22.0}],
            "coordinate_system": "EPSG:2113",
            "accuracy": {"horizontal_rmse_cm": 3.2, "vertical_rmse_cm": 4.1},
            "point_density_ppsm": 10.5,
            "files": [{"name": "scan.las", "format": "LAS"}],
        }
        spec = {
            "task_category": "site_survey",
            "capability_requirements": {
                "hard": {
                    "crs_epsg": 2113,
                    "asprs_vertical_class": "5cm",
                    "usgs_quality_level": "QL1",
                },
                "deliverables": [{"format": "LAS"}],
                "payload": {"fields": ["readings"]},
            },
        }
        result = check_delivery(data, spec)
        assert result.status == "PASS"
        assert result.level == 2

    def test_missing_crs_warns(self):
        data = {"readings": [{"temperature_c": 22.0}]}
        spec = {
            "capability_requirements": {
                "qa_level": 2,
                "hard": {"crs_epsg": 2113},
                "payload": {"fields": ["readings"]},
            },
        }
        result = check_delivery(data, spec)
        assert any("coordinate reference" in i.lower() for i in result.issues)

    def test_low_density_fails(self):
        data = {"readings": [{}], "point_density_ppsm": 1.0}
        spec = {
            "capability_requirements": {
                "qa_level": 2,
                "hard": {"usgs_quality_level": "QL1"},
                "payload": {"fields": ["readings"]},
            },
        }
        result = check_delivery(data, spec)
        assert result.status == "FAIL"
        assert any("density" in i.lower() for i in result.issues)

    def test_missing_accuracy_warns(self):
        data = {"readings": [{}]}
        spec = {
            "capability_requirements": {
                "qa_level": 2,
                "hard": {"asprs_vertical_class": "5cm"},
                "payload": {"fields": ["readings"]},
            },
        }
        result = check_delivery(data, spec)
        assert any("accuracy" in i.lower() for i in result.issues)


class TestLevel3:
    def test_pls_approved_passes(self):
        data = {"readings": [{}], "pls_review_status": "APPROVED"}
        spec = {"capability_requirements": {"qa_level": 3, "payload": {"fields": ["readings"]}}}
        result = check_delivery(data, spec)
        assert result.status == "PASS"
        assert result.level == 3

    def test_pls_pending_warns(self):
        data = {"readings": [{}], "pls_review_status": "PENDING"}
        spec = {"capability_requirements": {"qa_level": 3, "payload": {"fields": ["readings"]}}}
        result = check_delivery(data, spec)
        assert result.status == "WARN"

    def test_pls_missing_warns(self):
        data = {"readings": [{}]}
        spec = {"capability_requirements": {"qa_level": 3, "payload": {"fields": ["readings"]}}}
        result = check_delivery(data, spec)
        assert any("pls" in i.lower() for i in result.issues)

    def test_pls_rejected_fails(self):
        data = {"readings": [{}], "pls_review_status": "REJECTED"}
        spec = {"capability_requirements": {"qa_level": 3, "payload": {"fields": ["readings"]}}}
        result = check_delivery(data, spec)
        assert result.status == "FAIL"


class TestServerRoomDemo:
    """Verify the Tumbller server room demo passes QA at the right level."""

    def test_env_sensing_auto_selects_level_1(self):
        spec = {"task_category": "env_sensing", "capability_requirements": {}}
        assert get_qa_level(spec) == 1

    def test_tumbller_delivery_passes(self):
        data = {
            "readings": [
                {"waypoint": 1, "temperature_c": 22.4, "humidity_pct": 45.2},
                {"waypoint": 2, "temperature_c": 23.1, "humidity_pct": 43.8},
                {"waypoint": 3, "temperature_c": 21.9, "humidity_pct": 46.5},
            ],
            "summary": "All readings within spec.",
            "duration_seconds": 180,
            "robot_id": "989",
            "robot_name": "Tumbller Self-Balancing Robot",
        }
        spec = {
            "task_category": "env_sensing",
            "capability_requirements": {
                "payload": {"format": "json", "fields": ["readings", "summary"]},
            },
        }
        result = check_delivery(data, spec)
        assert result.passed
        assert result.level == 1


class TestQAResult:
    def test_to_dict(self):
        r = QAResult(status="PASS", level=1, checks_run=["data_exists"], details={"field_count": 3})
        d = r.to_dict()
        assert d["status"] == "PASS"
        assert d["level_name"] == "basic"
        assert d["passed"] is True

    def test_fail_not_passed(self):
        r = QAResult(status="FAIL", level=2, issues=["bad data"])
        assert not r.passed

    def test_warn_is_passed(self):
        r = QAResult(status="WARN", level=1, issues=["minor concern"])
        assert r.passed


# ════════════════════════════════════════════════════════════════════
# Section 2: Schema Validation Tests
# ════════════════════════════════════════════════════════════════════


class TestSchemaValidator:
    """Test the generic schema-driven delivery validation."""

    TUMBLLER_SCHEMA = {
        "description": "3 waypoint readings with temperature and humidity",
        "required": ["readings", "summary", "duration_seconds"],
        "properties": {
            "readings": {
                "type": "array",
                "minItems": 3,
                "items": {
                    "required": ["waypoint", "temperature_c", "humidity_pct", "timestamp"],
                    "properties": {
                        "temperature_c": {"type": "number", "minimum": -40, "maximum": 85},
                        "humidity_pct": {"type": "number", "minimum": 0, "maximum": 100},
                        "waypoint": {"type": "integer", "minimum": 1},
                        "timestamp": {"type": "string"},
                    },
                },
            },
            "summary": {"type": "string", "minLength": 1},
            "duration_seconds": {"type": "number", "minimum": 0},
        },
    }

    TUMBLLER_GOOD_DATA = {
        "readings": [
            {"waypoint": 1, "temperature_c": 22.4, "humidity_pct": 45.2, "timestamp": "2026-04-05T10:00:00Z"},
            {"waypoint": 2, "temperature_c": 23.1, "humidity_pct": 43.8, "timestamp": "2026-04-05T10:02:00Z"},
            {"waypoint": 3, "temperature_c": 21.9, "humidity_pct": 46.5, "timestamp": "2026-04-05T10:04:00Z"},
        ],
        "summary": "All readings within spec.",
        "duration_seconds": 240,
    }

    def test_valid_delivery_passes(self):
        issues = validate_delivery_schema(self.TUMBLLER_GOOD_DATA, self.TUMBLLER_SCHEMA)
        assert issues == []

    def test_missing_required_field(self):
        data = {**self.TUMBLLER_GOOD_DATA}
        del data["summary"]
        issues = validate_delivery_schema(data, self.TUMBLLER_SCHEMA)
        assert any("Missing required field: summary" in i for i in issues)

    def test_too_few_readings(self):
        data = {
            **self.TUMBLLER_GOOD_DATA,
            "readings": self.TUMBLLER_GOOD_DATA["readings"][:2],
        }
        issues = validate_delivery_schema(data, self.TUMBLLER_SCHEMA)
        assert any("minimum 3" in i for i in issues)

    def test_temperature_out_of_range(self):
        bad_readings = [
            {"waypoint": 1, "temperature_c": 200, "humidity_pct": 45, "timestamp": "t1"},
            {"waypoint": 2, "temperature_c": 22, "humidity_pct": 45, "timestamp": "t2"},
            {"waypoint": 3, "temperature_c": 22, "humidity_pct": 45, "timestamp": "t3"},
        ]
        data = {**self.TUMBLLER_GOOD_DATA, "readings": bad_readings}
        issues = validate_delivery_schema(data, self.TUMBLLER_SCHEMA)
        assert any("above maximum" in i for i in issues)

    def test_humidity_negative(self):
        bad_readings = [
            {"waypoint": 1, "temperature_c": 22, "humidity_pct": -5, "timestamp": "t1"},
            {"waypoint": 2, "temperature_c": 22, "humidity_pct": 45, "timestamp": "t2"},
            {"waypoint": 3, "temperature_c": 22, "humidity_pct": 45, "timestamp": "t3"},
        ]
        data = {**self.TUMBLLER_GOOD_DATA, "readings": bad_readings}
        issues = validate_delivery_schema(data, self.TUMBLLER_SCHEMA)
        assert any("below minimum" in i for i in issues)

    def test_missing_field_in_reading(self):
        bad_readings = [
            {"waypoint": 1, "temperature_c": 22, "timestamp": "t1"},
            {"waypoint": 2, "temperature_c": 22, "humidity_pct": 45, "timestamp": "t2"},
            {"waypoint": 3, "temperature_c": 22, "humidity_pct": 45, "timestamp": "t3"},
        ]
        data = {**self.TUMBLLER_GOOD_DATA, "readings": bad_readings}
        issues = validate_delivery_schema(data, self.TUMBLLER_SCHEMA)
        assert any("humidity_pct" in i for i in issues)

    def test_wrong_type(self):
        data = {**self.TUMBLLER_GOOD_DATA, "duration_seconds": "not a number"}
        issues = validate_delivery_schema(data, self.TUMBLLER_SCHEMA)
        assert any("Expected number" in i for i in issues)

    def test_empty_summary(self):
        data = {**self.TUMBLLER_GOOD_DATA, "summary": ""}
        issues = validate_delivery_schema(data, self.TUMBLLER_SCHEMA)
        assert any("too short" in i for i in issues)

    def test_robot_self_check_matches_qa(self):
        """Robot running self-check gets same result as marketplace QA."""
        self_issues = validate_delivery_schema(self.TUMBLLER_GOOD_DATA, self.TUMBLLER_SCHEMA)
        spec = {
            "task_category": "env_sensing",
            "capability_requirements": {"delivery_schema": self.TUMBLLER_SCHEMA},
        }
        qa_result = check_delivery(self.TUMBLLER_GOOD_DATA, spec, qa_level=1)
        assert self_issues == []
        assert qa_result.status == "PASS"

    def test_schema_driven_qa_catches_bad_delivery(self):
        """Full QA flow with schema catches incomplete delivery."""
        bad_data = {"readings": [], "summary": ""}
        spec = {
            "task_category": "env_sensing",
            "capability_requirements": {"delivery_schema": self.TUMBLLER_SCHEMA},
        }
        result = check_delivery(bad_data, spec, qa_level=1)
        assert result.status == "FAIL"
        assert len(result.issues) >= 2

    def test_no_schema_falls_back_to_legacy(self):
        """Without delivery_schema, Level 1 uses legacy field checks."""
        data = {"temperature_c": 22.5, "humidity_pct": 45.0}
        spec = {
            "task_category": "env_sensing",
            "capability_requirements": {
                "payload": {"format": "json", "fields": ["temperature_c", "humidity_pct"]},
            },
        }
        result = check_delivery(data, spec, qa_level=1)
        assert result.status == "PASS"
        assert "required_fields" in result.checks_run


class TestSurveySchema:
    """Test schema validation for construction survey deliverables."""

    SURVEY_SCHEMA = {
        "required": ["coordinate_system", "files"],
        "properties": {
            "coordinate_system": {"type": "string", "minLength": 1},
            "files": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "required": ["name", "format"],
                    "properties": {
                        "name": {"type": "string", "minLength": 1},
                        "format": {"type": "string", "minLength": 1},
                    },
                },
            },
        },
    }

    def test_valid_survey_delivery(self):
        data = {
            "coordinate_system": "EPSG:2113",
            "files": [
                {"name": "point_cloud.las", "format": "LAS 1.4"},
                {"name": "ortho.tiff", "format": "GeoTIFF"},
            ],
        }
        issues = validate_delivery_schema(data, self.SURVEY_SCHEMA)
        assert issues == []

    def test_missing_files(self):
        data = {"coordinate_system": "EPSG:2113", "files": []}
        issues = validate_delivery_schema(data, self.SURVEY_SCHEMA)
        assert any("minimum 1" in i for i in issues)

    def test_file_missing_format(self):
        data = {
            "coordinate_system": "EPSG:2113",
            "files": [{"name": "scan.las"}],
        }
        issues = validate_delivery_schema(data, self.SURVEY_SCHEMA)
        assert any("format" in i for i in issues)


# ════════════════════════════════════════════════════════════════════
# Section 3: Category Schema Tests (parametrized)
# ════════════════════════════════════════════════════════════════════

# -- Data generators (mirrors category_server.py) --


def _sim_gps(lat=42.5, lng=-83.5):
    return {
        "latitude": round(lat + random.uniform(-0.01, 0.01), 6),
        "longitude": round(lng + random.uniform(-0.01, 0.01), 6),
        "altitude_m": round(random.uniform(50, 120), 1),
        "fix": "RTK_FIXED",
        "satellites": random.randint(12, 24),
    }


def _make_aerial_lidar():
    area = random.randint(20000, 80000)
    density = round(random.uniform(2.0, 12.0), 1)
    return {
        "point_cloud": {
            "format": "LAS 1.4", "version": "1.4", "point_count": int(area * density),
            "density_pts_m2": density, "area_m2": area,
            "classifications": ["ground", "low_vegetation", "medium_vegetation",
                                "high_vegetation", "building", "noise"],
            "bounding_box": {"min": _sim_gps(), "max": _sim_gps()},
        },
        "quality_metrics": {
            "horizontal_accuracy_cm": round(random.uniform(2.0, 3.5), 1),
            "vertical_accuracy_cm": round(random.uniform(3.0, 5.0), 1),
            "control_points_used": random.randint(6, 15),
            "overlap_pct": random.randint(60, 75),
        },
        "coordinate_system": {"epsg": 2253, "datum": "NAD83(2011)",
                              "projection": "Michigan State Plane South"},
        "summary": f"Aerial LiDAR survey complete. {random.randint(3, 8)} flight lines captured.",
    }


def _make_aerial_photo():
    return {
        "orthomosaic": {
            "format": "GeoTIFF", "gsd_cm": round(random.uniform(0.8, 3.5), 2),
            "width_px": random.randint(10000, 50000), "height_px": random.randint(8000, 40000),
            "bands": 4, "bounding_box": {"min": _sim_gps(), "max": _sim_gps()},
        },
        "photo_set": {
            "total_photos": random.randint(80, 400), "overlap_frontal_pct": random.randint(75, 85),
            "overlap_side_pct": random.randint(65, 75), "camera_model": "DJI Zenmuse P1 / FC6360",
        },
        "quality_metrics": {
            "horizontal_accuracy_cm": round(random.uniform(1, 4), 1),
            "vertical_accuracy_cm": round(random.uniform(2, 6), 1),
            "reprojection_error_px": round(random.uniform(0.3, 0.8), 2),
            "ground_control_points": random.randint(4, 10),
        },
        "summary": f"Photogrammetry complete. {random.randint(80, 400)} photos processed.",
    }


def _make_ground_gpr():
    utilities = [
        {"type": random.choice(["water", "sewer", "electric", "gas", "telecom"]),
         "depth_m": round(random.uniform(0.3, 2.5), 2),
         "confidence": round(random.uniform(0.6, 0.98), 2),
         "apwa_color": random.choice(["blue", "green", "red", "yellow", "orange"]),
         "position": _sim_gps()}
        for _ in range(random.randint(2, 8))
    ]
    return {
        "scan_data": {"format": "DZT", "scan_lines": random.randint(10, 60),
                      "total_length_m": round(random.uniform(50, 500), 1),
                      "depth_m": round(random.uniform(1, 3), 1), "antenna_frequency_mhz": 1600},
        "utility_detections": utilities,
        "survey_parameters": {"coordinate_system": "EPSG:2253 Michigan State Plane South",
                              "accuracy_horizontal_cm": 15, "accuracy_depth_pct": 10,
                              "asce_38_quality_level": "B"},
        "summary": f"GPR survey complete. {len(utilities)} utilities detected.",
    }


def _make_aerial_thermal():
    anomalies = [
        {"severity": random.choice(["low", "medium", "high", "critical"]),
         "delta_t_c": round(random.uniform(2, 15), 1),
         "area_m2": round(random.uniform(0.5, 20), 1),
         "classification": random.choice(["moisture", "insulation_gap", "membrane_failure"]),
         "position": _sim_gps()}
        for _ in range(random.randint(1, 5))
    ]
    return {
        "thermal_mosaic": {"format": "RJPEG", "resolution": "640x512",
                           "temp_range_c": {"min": round(random.uniform(-5, 10), 1),
                                            "max": round(random.uniform(30, 65), 1)},
                           "emissivity": 0.95, "images_captured": random.randint(50, 200)},
        "anomalies": anomalies,
        "survey_conditions": {"ambient_temp_c": round(random.uniform(5, 25), 1),
                              "wind_speed_mph": round(random.uniform(2, 12), 1),
                              "sky_condition": random.choice(["clear", "partly_cloudy", "overcast"]),
                              "time_of_day": "pre-dawn"},
        "summary": f"Thermal survey complete. {len(anomalies)} anomalies detected.",
    }


def _make_bridge_inspection():
    elements = [
        {"element": elem, "condition_state": random.randint(1, 4),
         "quantity_pct": round(random.uniform(60, 100), 1),
         "defects": random.sample(["spalling", "cracking", "corrosion", "delamination",
                                    "efflorescence"], random.randint(0, 3))}
        for elem in ["deck", "superstructure", "substructure", "bearings", "joints"]
    ]
    return {
        "inspection_set": {"total_images": random.randint(100, 400),
                           "coverage_pct": round(random.uniform(85, 99), 1),
                           "resolution_mp": 48, "gsd_mm": round(random.uniform(0.5, 2), 1)},
        "element_ratings": elements,
        "summary": f"Bridge inspection complete. {len(elements)} elements rated per NBI coding.",
    }


def _make_ground_lidar():
    positions = [
        {"position_id": i + 1, "point_count": random.randint(500000, 2000000),
         "overlap_pct": round(random.uniform(30, 60), 1)}
        for i in range(random.randint(5, 15))
    ]
    return {
        "point_cloud": {"format": "E57", "point_count": sum(p["point_count"] for p in positions),
                        "scan_positions": len(positions),
                        "registration_error_mm": round(random.uniform(1, 5), 1)},
        "scan_positions": positions,
        "quality_metrics": {"registration_error_mm": round(random.uniform(1, 5), 1),
                            "coverage_pct": round(random.uniform(90, 99), 1)},
        "summary": f"Ground LiDAR scan complete. {len(positions)} positions registered.",
    }


def _make_confined():
    return {
        "point_cloud": {"format": "PLY", "point_count": random.randint(100000, 1000000),
                        "positioning_method": "SLAM",
                        "slam_confidence": round(random.uniform(0.75, 0.98), 2)},
        "inspection_photos": {"total_photos": random.randint(30, 150),
                              "lighting": "onboard_led", "resolution_mp": 12},
        "obstacle_map": {"obstacles_detected": random.randint(0, 8),
                         "clearance_min_m": round(random.uniform(0.5, 3), 1)},
        "summary": "Confined space inspection complete. SLAM-based positioning.",
    }


def _make_env_sensing():
    readings = [
        {"waypoint": i + 1, "temperature_c": round(random.uniform(18, 32), 1),
         "humidity_pct": round(random.uniform(30, 70), 1), "timestamp": str(time.time() + i * 60)}
        for i in range(3)
    ]
    return {"readings": readings, "summary": "Environmental readings captured at 3 waypoints.",
            "duration_seconds": round(random.uniform(10, 120), 1)}


def _make_ground_delivery():
    start_ts = int(time.time() * 1000)
    commands = ["forward", "left", "forward", "right", "stop"]
    command_log = [
        {"command": cmd, "timestamp_ms": start_ts + i * 1000,
         "duration_ms": random.randint(200, 1500)}
        for i, cmd in enumerate(commands)
    ]
    return {
        "task_id": f"task_{random.randint(1000, 9999)}", "commands_executed": command_log,
        "duration_s": round(sum(c["duration_ms"] for c in command_log) / 1000.0, 2),
        "completion_status": "completed", "robot_id": "8453:42",
        "summary": f"Executed {len(commands)} motor commands.",
    }


def _make_corridor():
    base = _make_aerial_lidar()
    base["corridor_metrics"] = {
        "length_m": round(random.uniform(500, 5000), 1),
        "width_m": round(random.uniform(20, 60), 1),
        "cross_sections": random.randint(10, 100),
        "cross_section_interval_m": round(random.uniform(10, 50), 1),
    }
    return base


# Schema name, generator, and expected category mappings
CATEGORY_CASES = [
    ("aerial_lidar", AERIAL_LIDAR_SCHEMA, _make_aerial_lidar,
     ["topo_survey", "aerial_survey", "volumetric", "site_survey", "control_survey", "mapping"]),
    ("aerial_photo", AERIAL_PHOTO_SCHEMA, _make_aerial_photo,
     ["progress_monitoring", "visual_inspection", "environmental_survey"]),
    ("ground_gpr", GROUND_GPR_SCHEMA, _make_ground_gpr,
     ["subsurface_scan", "utility_detection"]),
    ("aerial_thermal", AERIAL_THERMAL_SCHEMA, _make_aerial_thermal,
     ["thermal_inspection"]),
    ("bridge_inspection", BRIDGE_INSPECTION_SCHEMA, _make_bridge_inspection,
     ["bridge_inspection"]),
    ("ground_lidar", GROUND_LIDAR_SCHEMA, _make_ground_lidar,
     ["as_built"]),
    ("confined", CONFINED_SCHEMA, _make_confined,
     ["confined_space"]),
    ("env_sensing", ENV_SENSING_SCHEMA, _make_env_sensing,
     ["env_sensing", "sensor_reading"]),
    ("corridor", CORRIDOR_SCHEMA, _make_corridor,
     ["corridor_survey"]),
    ("ground_delivery", GROUND_DELIVERY_SCHEMA, _make_ground_delivery,
     ["delivery_ground"]),
]


class TestCategorySchemas:
    """Parametrized schema validation across all delivery categories."""

    @pytest.fixture(autouse=True)
    def seed_random(self):
        random.seed(42)

    @pytest.mark.parametrize("name,schema,generator,categories", CATEGORY_CASES,
                             ids=[c[0] for c in CATEGORY_CASES])
    def test_schema_passes(self, name, schema, generator, categories):
        data = generator()
        issues = validate_delivery_schema(data, schema)
        assert issues == [], f"{name} schema failed: {issues}"

    @pytest.mark.parametrize("name,schema,generator,categories", CATEGORY_CASES,
                             ids=[c[0] for c in CATEGORY_CASES])
    def test_category_mapping(self, name, schema, generator, categories):
        for cat in categories:
            assert get_delivery_schema(cat) == schema, f"{cat} should map to {name} schema"


class TestGroundDeliveryEdgeCases:
    """Extra edge-case tests for ground delivery schema."""

    @pytest.fixture(autouse=True)
    def seed_random(self):
        random.seed(42)

    def test_missing_required_field_fails(self):
        data = _make_ground_delivery()
        del data["commands_executed"]
        issues = validate_delivery_schema(data, GROUND_DELIVERY_SCHEMA)
        assert any("commands_executed" in i for i in issues), (
            f"Expected missing-field issue for commands_executed, got: {issues}"
        )

    def test_empty_command_log_fails(self):
        data = _make_ground_delivery()
        data["commands_executed"] = []
        issues = validate_delivery_schema(data, GROUND_DELIVERY_SCHEMA)
        assert any("minimum 1" in i for i in issues), (
            f"Expected minItems violation for empty commands_executed, got: {issues}"
        )


class TestAllCategoriesCovered:
    """Verify every task category in the mapping has a test."""

    def test_all_categories_mapped(self):
        from auction.delivery_schemas import DELIVERY_SCHEMAS

        assert len(DELIVERY_SCHEMAS) == 19
        for cat in DELIVERY_SCHEMAS:
            schema = get_delivery_schema(cat)
            assert schema is not None, f"No schema for {cat}"
