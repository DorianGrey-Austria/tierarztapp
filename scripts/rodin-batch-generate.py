#!/usr/bin/env python3
"""
Batch-generate 3D models via Blender MCP + Hyper3D Rodin API.
Usage: python3 scripts/rodin-batch-generate.py <batch_file.json> [--download]
"""
import socket, json, time, sys, os

PROJECT = "/Users/cardrevolution/Desktop/coding/tierarztapp"

def send_cmd(cmd, timeout=20):
    """Send command to Blender MCP, fresh connection per call."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 9876))
    time.sleep(0.3)
    sock.sendall(json.dumps(cmd).encode('utf-8'))
    time.sleep(4)
    data = b''
    sock.settimeout(timeout)
    try:
        while True:
            chunk = sock.recv(65536)
            if not chunk:
                break
            data += chunk
    except socket.timeout:
        pass
    sock.close()
    if data:
        decoder = json.JSONDecoder()
        result, _ = decoder.raw_decode(data.decode('utf-8'))
        return result
    return None

def submit_job(prompt):
    """Submit a Rodin generation job, return uuid."""
    r = send_cmd({
        'type': 'create_rodin_job',
        'params': {'text_prompt': prompt}
    })
    if r and r.get('status') == 'success':
        return r['result'].get('uuid', '')
    return None

def download_glb(uuid, output_path, api_timeout=90):
    """Download GLB via Blender's Python (has the API key)."""
    code = f'''
import requests, bpy, os
api_key = bpy.context.scene.blendermcp_hyper3d_api_key
r = requests.post("https://hyperhuman.deemos.com/api/v2/download",
    headers={{"Authorization": f"Bearer {{api_key}}"}},
    json={{"task_uuid": "{uuid}"}}, timeout=15)
data = r.json()
glb_url = None
for item in data.get("list", []):
    if item["name"].endswith(".glb"):
        glb_url = item["url"]
        break
if not glb_url:
    print("NOT_READY")
else:
    os.makedirs(os.path.dirname("{output_path}"), exist_ok=True)
    resp = requests.get(glb_url, stream=True, timeout=60)
    resp.raise_for_status()
    with open("{output_path}", "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    sz = os.path.getsize("{output_path}")
    print(f"OK {{sz//1024}}KB")
'''
    r = send_cmd({'type': 'execute_code', 'params': {'code': code}}, timeout=api_timeout)
    if r:
        result = r.get('result', {}).get('result', '')
        return result
    return 'NO_RESPONSE'

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/rodin-batch-generate.py <batch.json> [--download]")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        batch = json.load(f)

    download_mode = '--download' in sys.argv

    if download_mode:
        # Download mode: read jobs file and download GLBs
        jobs_file = sys.argv[1].replace('.json', '_jobs.json')
        with open(jobs_file) as f:
            jobs = json.load(f)
        for job in jobs:
            output = os.path.join(PROJECT, job['output'])
            if os.path.exists(output):
                print(f"  SKIP {job['name']} (exists)")
                continue
            result = download_glb(job['uuid'], output)
            print(f"  {job['name']}: {result}")
            time.sleep(1)
    else:
        # Submit mode
        jobs = []
        for item in batch:
            print(f"Submitting: {item['name']}...", end=' ', flush=True)
            uuid = submit_job(item['prompt'])
            if uuid:
                jobs.append({**item, 'uuid': uuid})
                print(f"OK ({uuid[:12]}...)")
            else:
                print("FAIL")
            time.sleep(1)

        # Save jobs
        jobs_file = sys.argv[1].replace('.json', '_jobs.json')
        with open(jobs_file, 'w') as f:
            json.dump(jobs, f, indent=2)
        print(f"\n{len(jobs)}/{len(batch)} submitted -> {jobs_file}")
