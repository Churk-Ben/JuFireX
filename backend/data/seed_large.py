import os
import sys
import random
import shutil
import uuid
import json
from pathlib import Path
from datetime import datetime

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from backend.app import create_app
from backend.config import Config, ROLE_MEMBER
from backend.data.database import db
from backend.data.models.user import User
from backend.data.models.blog import Blog
from backend.data.models.project import Project
from backend.data.models.navigation import Navigation

# Source for avatars
AVATAR_SOURCE_DIR = Path(r"D:\Pictures\存图\头像")


def get_random_avatar():
    if not AVATAR_SOURCE_DIR.exists():
        return None
    files = [
        f
        for f in AVATAR_SOURCE_DIR.iterdir()
        if f.is_file() and f.suffix.lower() in [".jpg", ".jpeg", ".png"]
    ]
    if not files:
        return None
    return random.choice(files)


def generate_random_string(length=10):
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(random.choice(charset) for _ in range(length))


def generate_random_chinese_string(length=5):
    # Basic range of common Chinese characters
    val = [chr(random.randint(0x4E00, 0x9FBF)) for _ in range(length)]
    return "".join(val)


def seed_users(count=100):
    print(f"Generating {count} users...")
    users = []
    for i in range(count):
        username = f"user_{generate_random_string(5)}_{i}"
        email = f"{username}@example.com"
        user = User(username=username, email=email, role=ROLE_MEMBER, is_active=True)
        user.set_password("password")
        db.session.add(user)
        users.append(user)

    db.session.commit()

    # Process avatars after commit to have UUIDs (though UUID is generated on init, let's be safe)
    for user in users:
        # Create user directory
        user_dir = Config.PROFILES_DIR / user.uuid
        user_dir.mkdir(parents=True, exist_ok=True)

        # Copy avatar
        avatar_src = get_random_avatar()
        if avatar_src:
            shutil.copy(avatar_src, user_dir / "avatar.png")

    print(f"Created {len(users)} users.")
    return users


def seed_blogs(users, count_per_user=10):
    print(f"Generating blogs ({len(users) * count_per_user} total)...")
    total = 0
    for user in users:
        for _ in range(count_per_user):
            blog_uuid = str(uuid.uuid4())
            title = (
                f"Blog {generate_random_chinese_string(5)} {generate_random_string(5)}"
            )
            summary = f"Summary for {title}"
            content = f"# {title}\n\nThis is a generated blog post.\n\n{generate_random_string(100)}"

            # DB Record
            blog = Blog(
                uuid=blog_uuid,
                owner_uuid=user.uuid,
                is_public=True,
                views=random.randint(0, 1000),
            )
            db.session.add(blog)

            # Files
            blog_dir = Config.BLOGS_DIR / blog_uuid
            blog_dir.mkdir(parents=True, exist_ok=True)

            metadata = {
                "title": title,
                "summary": summary,
                "tags": ["generated", "test", generate_random_string(3)],
                "cover_image": "",
                "author_name": user.username,
            }

            with (blog_dir / "metadata.json").open("w", encoding="utf-8") as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)

            with (blog_dir / "article.md").open("w", encoding="utf-8") as f:
                f.write(content)

            total += 1

        # Commit in batches per user to avoid huge transaction
        db.session.commit()

    print(f"Created {total} blogs.")


def seed_projects(count=200):
    print(f"Generating {count} projects...")
    for _ in range(count):
        project = Project(
            title=f"Project {generate_random_chinese_string(3)}",
            description=f"Description {generate_random_string(20)}",
            content=f"Content {generate_random_string(50)}",
            url="http://example.com",
            tags="generated,test",
            is_public=True,
        )
        db.session.add(project)
    db.session.commit()
    print("Projects created.")


def seed_navigations(users, count=200):
    print(f"Generating {count} navigations...")
    for _ in range(count):
        user = random.choice(users) if random.random() > 0.5 else None
        nav = Navigation(
            title=f"Nav {generate_random_string(5)}",
            url="http://example.com",
            description="Generated navigation",
            category="Tools",
            owner_uuid=user.uuid if user else None,
            is_public=True,
        )
        db.session.add(nav)
    db.session.commit()
    print("Navigations created.")


def main():
    app = create_app()
    with app.app_context():
        print("Starting data generation...")

        # Verify avatar source
        if not AVATAR_SOURCE_DIR.exists():
            print(
                f"Warning: Avatar source directory {AVATAR_SOURCE_DIR} does not exist. Avatars will not be set."
            )
        else:
            print(f"Found avatar source: {AVATAR_SOURCE_DIR}")

        users = seed_users(100)
        seed_blogs(users, 10)
        seed_projects(200)
        seed_navigations(users, 200)

        print("Data generation complete.")


if __name__ == "__main__":
    main()
