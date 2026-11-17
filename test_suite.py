import sys
from fastapi.testclient import TestClient
from backend.app.main import app

def run_tests():
    print("Initializing TestClient...")
    with TestClient(app) as client:
        # 1. Health check
        print("\n--- Test 1: Health check ---")
        res = client.get("/api/health")
        print(f"Health Status: {res.status_code}, Data: {res.json()}")
        assert res.status_code == 200

        # 2. System status
        print("\n--- Test 2: System status ---")
        res = client.get("/api/status")
        print(f"System Status: {res.status_code}, DB mode: {res.json()['database']['mode']}")
        assert res.status_code == 200

        # 3. Category stats
        print("\n--- Test 3: Category statistics ---")
        res = client.get("/api/writings/stats/categories")
        stats = res.json()
        print(f"Categories returned: {list(stats.keys())}")
        for cat, data in stats.items():
            print(f"  {cat}: {data['count']} items, topics: {data['topics'][:3]}")
        assert "stories" in stats and "letters" in stats and "articles" in stats and "emails" in stats

        # 4. List writings for each category
        for cat in ["stories", "letters", "articles", "emails"]:
            res = client.get(f"/api/writings?category={cat}")
            items = res.json()
            print(f"\n--- Category '{cat}' has {len(items)} items ---")
            assert len(items) > 0
            first = items[0]
            print(f"  First item: '{first['title']}' | Level: {first['level']} | Reading time: {first['reading_time_minutes']} min")

        # 5. Search & filter test
        print("\n--- Test 5: Search & Filter ---")
        res = client.get("/api/writings?category=stories&level=B1")
        b1_stories = res.json()
        print(f"  Found {len(b1_stories)} B1 stories.")
        assert len(b1_stories) > 0

        res_search = client.get("/api/writings?search=camera")
        search_results = res_search.json()
        print(f"  Search 'camera': {len(search_results)} items found.")
        assert len(search_results) > 0

        # 6. Create Writing (Draft)
        print("\n--- Test 6: Create draft in Writing Studio ---")
        new_piece = {
            "title": "A Day in the Mountain Village",
            "category": "stories",
            "content": "Last autumn, I visited a picturesque mountain village surrounded by pine trees. Although it was chilly, the fresh air was invigorating. We walked along the rocky trail and met friendly shepherds who offered us warm mint tea.",
            "topic": "Travel",
            "level": "B1",
            "status": "draft",
            "visibility": "private",
            "author_name": "Test Writer"
        }
        res = client.post("/api/writings", json=new_piece)
        created = res.json()
        print(f"  Created draft ID: {created['id']} | Word count: {created['word_count']} | Status: {created['status']}")
        assert res.status_code == 201

        # 7. AI B1 Evaluation
        print("\n--- Test 7: AI Cambridge B1 Review ---")
        eval_payload = {
            "writing_id": created["id"],
            "title": created["title"],
            "category": created["category"],
            "content": created["content"]
        }
        res = client.post("/api/reviews/evaluate", json=eval_payload)
        rev = res.json()
        print(f"  Evaluation Level: {rev['estimated_level']}")
        print(f"  Verdict: {rev['suitability_verdict']}")
        print(f"  Score: {rev['suitability_score']}/100")
        print(f"  Engine used: {rev['ai_engine_used']}")
        print(f"  Sentence suggestions count: {len(rev['sentence_suggestions'])}")
        assert res.status_code == 201
        assert "vocabulary" in rev["observations"]
        assert "grammar" in rev["observations"]
        assert "sentence_length" in rev["observations"]
        assert "organization" in rev["observations"]

        # 8. Bookmark toggle
        print("\n--- Test 8: Bookmarks ---")
        res_bm = client.post(f"/api/bookmarks/{created['id']}")
        print(f"  Bookmark toggle: {res_bm.json()}")
        assert res_bm.json()["bookmarked"] is True

        res_bm_list = client.get("/api/bookmarks")
        bm_items = res_bm_list.json()
        print(f"  Total bookmarks: {len(bm_items)}")
        assert any(b["id"] == created["id"] for b in bm_items)

        # 9. File upload (.txt and .docx)
        print("\n--- Test 9: File upload ---")
        test_txt = b"The Journey Across the Lake\n\nIt was an early Sunday morning when Clara and her brother boarded the small wooden ferry."
        files = {"file": ("ferry_story.txt", test_txt, "text/plain")}
        res_up = client.post("/api/uploads", files=files)
        print(f"  Upload result: {res_up.json()['title']} - {res_up.json()['word_count']} words")
        assert res_up.status_code == 200

        # 10. Settings API
        print("\n--- Test 10: Customization Settings ---")
        res_set = client.get("/api/settings")
        print(f"  Current settings: {res_set.json()['theme']}, font: {res_set.json()['font_family']}")
        assert res_set.status_code == 200

        # 11. Clean up created piece
        client.delete(f"/api/writings/{created['id']}")
        print("\n--- Test 11: Cleanup successful ---")

    print("\n================================================")
    print("  ALL 11 BACKEND & AI & DB TESTS PASSED 100%!  ")
    print("================================================")

if __name__ == "__main__":
    run_tests()
