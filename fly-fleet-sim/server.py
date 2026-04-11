"""
Multi-category robot fleet simulator.

Single FastMCP server with mounted sub-servers per robot category.
Each category's tools are namespaced (e.g., aerial_lidar_fly_waypoint).

Endpoints: /mcp (all tools via single MCP server)
Categories: aerial_lidar, aerial_photo, aerial_thermal, fixedwing,
            ground_lidar, ground_gpr, confined, skydio, fakerover
"""

import random
import time
import os

from fastmcp import FastMCP


# ── Simulated data generators ──────────────────────────────────────

def sim_gps(base_lat=42.5, base_lng=-83.5):
    return {"latitude": round(base_lat + random.uniform(-0.01, 0.01), 6),
            "longitude": round(base_lng + random.uniform(-0.01, 0.01), 6),
            "altitude_m": round(random.uniform(50, 120), 1), "fix": "RTK_FIXED",
            "satellites": random.randint(12, 24), "hdop": round(random.uniform(0.5, 1.2), 2)}

def sim_battery():
    return {"level_pct": random.randint(40, 100), "voltage_v": round(random.uniform(21.5, 25.2), 1),
            "temperature_c": round(random.uniform(22, 38), 1), "estimated_flight_min": random.randint(8, 45)}

def sim_lidar():
    return {"points_captured": random.randint(800_000, 4_200_000), "density_pts_m2": round(random.uniform(5, 25), 1),
            "accuracy_cm": round(random.uniform(1.5, 4.0), 1), "format": "LAS 1.4", "timestamp": time.time()}

def sim_photo():
    return {"resolution_mp": random.choice([20, 45, 48, 61]), "gsd_cm": round(random.uniform(0.8, 3.5), 2),
            "photos_captured": random.randint(1, 200), "format": "JPEG+RAW", "timestamp": time.time()}

def sim_thermal():
    return {"min_temp_c": round(random.uniform(-5, 15), 1), "max_temp_c": round(random.uniform(25, 85), 1),
            "avg_temp_c": round(random.uniform(18, 35), 1), "resolution": "640x512", "timestamp": time.time()}

def sim_gpr():
    return {"scan_length_m": round(random.uniform(5, 100), 1), "depth_m": round(random.uniform(0.3, 3.0), 1),
            "frequency_mhz": random.choice([400, 900, 1600]), "utilities_detected": random.randint(0, 8),
            "format": "DZT", "timestamp": time.time()}

def sim_wind():
    return {"speed_mph": round(random.uniform(2, 18), 1), "direction_deg": random.randint(0, 359),
            "gusts_mph": round(random.uniform(5, 25), 1)}


# ── Aerial LiDAR ──────────────────────────────────────────────────
aerial_lidar = FastMCP("Aerial LiDAR Simulator")

@aerial_lidar.tool
async def fly_waypoint(latitude: float, longitude: float, altitude_m: float = 80) -> dict:
    """Fly to a GPS waypoint at specified altitude."""
    return {"status": "arrived", "position": sim_gps(latitude, longitude)}

@aerial_lidar.tool
async def capture_lidar_scan(duration_seconds: int = 30) -> dict:
    """Capture a LiDAR point cloud scan."""
    return sim_lidar()

@aerial_lidar.tool
async def get_gps_position() -> dict:
    """Get current GPS position with RTK fix status."""
    return sim_gps()

@aerial_lidar.tool
async def check_battery() -> dict:
    """Check battery level and estimated flight time."""
    return sim_battery()

@aerial_lidar.tool
async def return_to_home() -> dict:
    """Return to launch point and land."""
    return {"status": "landing", "eta_seconds": random.randint(30, 120)}

@aerial_lidar.tool
async def set_flight_altitude(altitude_m: float) -> dict:
    """Set flight altitude in meters AGL."""
    return {"status": "altitude_set", "altitude_m": altitude_m}

@aerial_lidar.tool
async def get_wind_speed() -> dict:
    """Get current wind speed and direction."""
    return sim_wind()


# ── Aerial Photo ──────────────────────────────────────────────────
aerial_photo = FastMCP("Aerial Photogrammetry Simulator")

@aerial_photo.tool
async def fly_waypoint(latitude: float, longitude: float, altitude_m: float = 60) -> dict:
    """Fly to a GPS waypoint."""
    return {"status": "arrived", "position": sim_gps(latitude, longitude)}

@aerial_photo.tool
async def capture_photo() -> dict:
    """Capture a geotagged photo."""
    return sim_photo()

@aerial_photo.tool
async def capture_video(duration_seconds: int = 10) -> dict:
    """Record geotagged video."""
    return {"status": "recorded", "duration_s": duration_seconds, "resolution": "4K"}

@aerial_photo.tool
async def get_gps_position() -> dict:
    """Get current GPS position."""
    return sim_gps()

@aerial_photo.tool
async def check_battery() -> dict:
    """Check battery level."""
    return sim_battery()

@aerial_photo.tool
async def return_to_home() -> dict:
    """Return to launch point."""
    return {"status": "landing", "eta_seconds": random.randint(30, 120)}

@aerial_photo.tool
async def set_camera_params(iso: int = 100, shutter_speed: str = "1/1000", aperture: float = 2.8) -> dict:
    """Set camera parameters."""
    return {"status": "params_set", "iso": iso, "shutter_speed": shutter_speed, "aperture": aperture}


# ── Aerial Thermal ────────────────────────────────────────────────
aerial_thermal = FastMCP("Aerial Thermal Simulator")

@aerial_thermal.tool
async def fly_waypoint(latitude: float, longitude: float, altitude_m: float = 40) -> dict:
    """Fly to a GPS waypoint."""
    return {"status": "arrived", "position": sim_gps(latitude, longitude)}

@aerial_thermal.tool
async def capture_thermal() -> dict:
    """Capture thermal infrared image."""
    return sim_thermal()

@aerial_thermal.tool
async def capture_photo() -> dict:
    """Capture a visual photo."""
    return sim_photo()

@aerial_thermal.tool
async def get_surface_temp(latitude: float, longitude: float) -> dict:
    """Get surface temperature at a point."""
    return {"temperature_c": round(random.uniform(15, 65), 1), "position": sim_gps(latitude, longitude)}

@aerial_thermal.tool
async def get_gps_position() -> dict:
    """Get current GPS position."""
    return sim_gps()

@aerial_thermal.tool
async def check_battery() -> dict:
    """Check battery level."""
    return sim_battery()

@aerial_thermal.tool
async def return_to_home() -> dict:
    """Return to launch point."""
    return {"status": "landing", "eta_seconds": random.randint(30, 120)}


# ── Fixed-Wing ────────────────────────────────────────────────────
fixedwing = FastMCP("Fixed-Wing VTOL Simulator")

@fixedwing.tool
async def launch_vtol() -> dict:
    """VTOL launch sequence."""
    return {"status": "airborne", "altitude_m": 120, "mode": "cruise"}

@fixedwing.tool
async def fly_corridor(start_lat: float, start_lng: float, end_lat: float, end_lng: float, width_m: float = 100) -> dict:
    """Fly a corridor survey between two points."""
    return {"status": "corridor_complete", "distance_km": round(random.uniform(1, 20), 1), "photos": random.randint(50, 500)}

@fixedwing.tool
async def capture_photo() -> dict:
    """Capture a geotagged photo during flight."""
    return sim_photo()

@fixedwing.tool
async def get_gps_position() -> dict:
    """Get current GPS position."""
    return sim_gps()

@fixedwing.tool
async def check_battery() -> dict:
    """Check battery level."""
    return sim_battery()

@fixedwing.tool
async def land_vtol() -> dict:
    """VTOL landing sequence."""
    return {"status": "landed", "position": sim_gps()}

@fixedwing.tool
async def set_flight_plan(waypoints: list) -> dict:
    """Upload a flight plan."""
    return {"status": "plan_loaded", "waypoints": len(waypoints) if waypoints else 0}


# ── Ground LiDAR (Spot) ──────────────────────────────────────────
ground_lidar = FastMCP("Ground LiDAR Simulator")

@ground_lidar.tool
async def walk_to(latitude: float, longitude: float) -> dict:
    """Walk to a GPS position."""
    return {"status": "arrived", "position": sim_gps(latitude, longitude), "terrain": random.choice(["flat", "stairs", "rubble"])}

@ground_lidar.tool
async def scan_360_lidar() -> dict:
    """360-degree LiDAR scan."""
    return sim_lidar()

@ground_lidar.tool
async def capture_photo() -> dict:
    """Capture a photo."""
    return sim_photo()

@ground_lidar.tool
async def get_position() -> dict:
    """Get current position and heading."""
    p = sim_gps(); p["heading_deg"] = random.randint(0, 359); return p

@ground_lidar.tool
async def check_battery() -> dict:
    """Check battery and runtime."""
    b = sim_battery(); b["estimated_runtime_min"] = random.randint(30, 90); return b

@ground_lidar.tool
async def dock() -> dict:
    """Return to charging dock."""
    return {"status": "docking", "eta_seconds": random.randint(60, 300)}

@ground_lidar.tool
async def navigate_stairs(direction: str = "up") -> dict:
    """Navigate a staircase."""
    return {"status": "stairs_complete", "direction": direction}


# ── Ground GPR (Spot) ─────────────────────────────────────────────
ground_gpr = FastMCP("Ground GPR Simulator")

@ground_gpr.tool
async def walk_to(latitude: float, longitude: float) -> dict:
    """Walk to a GPS position."""
    return {"status": "arrived", "position": sim_gps(latitude, longitude)}

@ground_gpr.tool
async def deploy_gpr() -> dict:
    """Lower and calibrate GPR antenna."""
    return {"status": "gpr_deployed", "frequency_mhz": 1600, "calibration": "complete"}

@ground_gpr.tool
async def scan_gpr_line(length_m: float = 10, direction_deg: int = 0) -> dict:
    """Scan a GPR line."""
    return sim_gpr()

@ground_gpr.tool
async def get_position() -> dict:
    """Get current position."""
    return sim_gps()

@ground_gpr.tool
async def check_battery() -> dict:
    """Check battery level."""
    b = sim_battery(); b["estimated_runtime_min"] = random.randint(30, 90); return b

@ground_gpr.tool
async def dock() -> dict:
    """Return to charging dock."""
    return {"status": "docking", "eta_seconds": random.randint(60, 300)}

@ground_gpr.tool
async def mark_utility(depth_m: float, utility_type: str = "unknown") -> dict:
    """Mark a detected underground utility."""
    return {"status": "marked", "depth_m": depth_m, "type": utility_type, "position": sim_gps()}


# ── Confined Space (ELIOS 3) ─────────────────────────────────────
confined = FastMCP("Confined Space Simulator")

@confined.tool
async def fly_indoor(direction: str = "forward", distance_m: float = 5) -> dict:
    """Fly inside a confined space."""
    return {"status": "moved", "direction": direction, "distance_m": distance_m}

@confined.tool
async def capture_lidar_scan() -> dict:
    """LiDAR scan of enclosed space."""
    s = sim_lidar(); s["environment"] = "indoor"; return s

@confined.tool
async def capture_photo() -> dict:
    """Photo with onboard lighting."""
    p = sim_photo(); p["lighting"] = "onboard_led"; return p

@confined.tool
async def detect_obstacle() -> dict:
    """Detect obstacles in all directions."""
    return {d + "_m": round(random.uniform(0.3, 10), 1) for d in ["front", "rear", "left", "right"]}

@confined.tool
async def get_position() -> dict:
    """Estimated position (SLAM, GPS-denied)."""
    return {"x_m": round(random.uniform(0, 50), 1), "y_m": round(random.uniform(0, 30), 1), "z_m": round(random.uniform(0, 10), 1), "method": "SLAM"}

@confined.tool
async def check_battery() -> dict:
    """Check battery level."""
    return sim_battery()

@confined.tool
async def return_to_pilot() -> dict:
    """Retrace path to entry point."""
    return {"status": "returning", "eta_seconds": random.randint(30, 180)}


# ── Skydio X10 ────────────────────────────────────────────────────
skydio = FastMCP("Skydio X10 Simulator")

@skydio.tool
async def fly_waypoint(latitude: float, longitude: float, altitude_m: float = 40) -> dict:
    """Fly to a GPS waypoint with obstacle avoidance."""
    return {"status": "arrived", "position": sim_gps(latitude, longitude), "obstacle_avoidance": "active"}

@skydio.tool
async def fly_orbit(center_lat: float, center_lng: float, radius_m: float = 20, altitude_m: float = 30) -> dict:
    """Orbit a point of interest."""
    return {"status": "orbit_complete", "photos_captured": random.randint(12, 36), "radius_m": radius_m}

@skydio.tool
async def capture_photo() -> dict:
    """Capture a high-resolution photo."""
    return sim_photo()

@skydio.tool
async def capture_thermal() -> dict:
    """Capture thermal image."""
    return sim_thermal()

@skydio.tool
async def autonomous_inspect(structure_type: str = "bridge") -> dict:
    """Autonomous inspection scan."""
    return {"status": "inspection_complete", "structure": structure_type, "images_captured": random.randint(50, 200), "anomalies": random.randint(0, 5)}

@skydio.tool
async def get_gps_position() -> dict:
    """Get current GPS position."""
    return sim_gps()

@skydio.tool
async def check_battery() -> dict:
    """Check battery level."""
    return sim_battery()


# ── Legacy FakeRover ──────────────────────────────────────────────
fakerover = FastMCP("FakeRover Simulator")

@fakerover.tool
async def move(direction: str = "forward") -> dict:
    """Move the rover."""
    return {"status": "moved", "direction": direction, "distance_m": round(random.uniform(0.5, 2.0), 1)}

@fakerover.tool
async def is_online() -> dict:
    """Check if the rover is online."""
    return {"online": True}

@fakerover.tool
async def get_temperature_humidity() -> dict:
    """Read temperature and humidity."""
    return {"temperature_c": round(random.uniform(18, 32), 1), "humidity_pct": round(random.uniform(30, 70), 1)}


# ── Root server ───────────────────────────────────────────────────
mcp = FastMCP("yakrover Fleet Simulator")

mcp.mount(aerial_lidar, namespace="aerial_lidar")
mcp.mount(aerial_photo, namespace="aerial_photo")
mcp.mount(aerial_thermal, namespace="aerial_thermal")
mcp.mount(fixedwing, namespace="fixedwing")
mcp.mount(ground_lidar, namespace="ground_lidar")
mcp.mount(ground_gpr, namespace="ground_gpr")
mcp.mount(confined, namespace="confined")
mcp.mount(skydio, namespace="skydio")
mcp.mount(fakerover, namespace="fakerover")

@mcp.tool
async def health() -> dict:
    """Fleet simulator health check."""
    return {"status": "ok", "categories": 9}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="http", host="0.0.0.0", port=port)
