#!/usr/bin/env python3
"""
Deploy to Hugging Face Space
"""

import subprocess
import os
from pathlib import Path

def main():
    print("🚀 Deploying to Hugging Face Space")
    print("=" * 40)
    
    hf_space_dir = Path(__file__).parent / "hf-space-download"
    
    if not hf_space_dir.exists():
        print("❌ HF Space directory not found!")
        return
    
    os.chdir(hf_space_dir)
    
    print("📁 Current files:")
    for file in Path(".").iterdir():
        if not file.name.startswith('.'):
            print(f"   ✅ {file.name}")
    
    print("\n🔄 Git operations:")
    
    # Git add all files
    subprocess.run(["git", "add", "."])
    
    # Git commit
    commit_msg = input("\n💬 Commit message (default: 'Update with optimized lazy loading'): ")
    if not commit_msg.strip():
        commit_msg = "Update with optimized lazy loading"
    
    subprocess.run(["git", "commit", "-m", commit_msg])
    
    # Git push
    print("🚀 Pushing to Hugging Face Space...")
    result = subprocess.run(["git", "push"])
    
    if result.returncode == 0:
        print("\n✅ Successfully deployed!")
        print("🌐 Your Space: https://huggingface.co/spaces/t3k45h1/promptagrow")
        print("⏰ Build time: ~3-5 minutes")
        print("🔗 API URL: https://t3k45h1-promptagrow.hf.space")
    else:
        print("\n❌ Deployment failed. Check git credentials.")

if __name__ == "__main__":
    main()
