from sqlalchemy.orm import Session
from config.database import SessionLocal
from domain.ranking.ranking_crud import get_rankings, update_user_tier
from api.models import Tier

def reset_and_update_rankings():
    db = SessionLocal()
    rankings = get_rankings(db)
    total_users = len(rankings)
    if total_users == 0:
        db.close()
        return

    top_30_percent_index = total_users * 3 // 10
    bottom_30_percent_index = total_users * 7 // 10

    tier_order = [
        Tier.iron, Tier.bronze, Tier.silver, Tier.gold,
        Tier.platinum, Tier.emerald, Tier.diamond, Tier.master
    ]

    try:
        for i, user in enumerate(rankings):
            current_tier_index = tier_order.index(user.tier)
            if i < top_30_percent_index and user.tier != Tier.master:
                new_tier = tier_order[min(current_tier_index + 1, len(tier_order) - 1)]
            elif i >= bottom_30_percent_index and user.tier != Tier.iron:
                new_tier = tier_order[max(current_tier_index - 1, 0)]
            else:
                new_tier = user.tier  # 중간에 있는 유저는 티어가 변경되지 않음

            # 티어 업데이트 및 점수 초기화
            user.tier = new_tier
            user.score = 0
        
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    reset_and_update_rankings()
    print("Rankings have been reset and updated.")