from services.analysis_service import get_recent_trend, get_subject_statistics, get_task_type_statistics, get_time_period_statistics


class RecommendationService:
    def get_recommendations(self, user_id: int) -> list[str]:
        recs = []
        for item in get_subject_statistics(user_id):
            if item["count"] >= 5 and item["avg_rate"] > 20:
                recs.append(f"近期{item['name']}任务实际用时平均高于计划约 {item['avg_rate']:.0f}%，下次可适当增加计划时长。")
        for item in get_task_type_statistics(user_id):
            if item["count"] >= 5 and item["avg_rate"] > 40:
                recs.append(f"你在“{item['name']}”类任务上经常低估所需时间，建议增加时间余量。")
            elif item["count"] >= 5 and item["avg_rate"] < -20 and item["completion_rate"] >= 80:
                recs.append(f"“{item['name']}”通常比计划时间提前完成，且完成程度较高，后续可适当缩短安排。")
        periods = get_time_period_statistics(user_id); all_rate = sum(x["completion_rate"] for x in periods) / len(periods) if periods else 0
        for item in periods:
            if item["count"] >= 8 and item["completion_rate"] < all_rate - 15:
                recs.append(f"你的{item['name']}任务执行完成率相对较低，重要任务可以尝试提前安排。")
        trend = get_recent_trend(user_id, 14)
        recent = [x["avg_rate"] for x in trend[-7:] if x["avg_rate"]]
        previous = [x["avg_rate"] for x in trend[:7] if x["avg_rate"]]
        if recent and previous and sum(abs(x) for x in recent) / len(recent) < sum(abs(x) for x in previous) / len(previous) * .8:
            recs.append("最近一周计划时间与实际执行更加接近，你的学习时间估计正在逐步改善。")
        return recs or ["继续记录学习任务后，系统将逐步生成个性化建议。"]

    def suggest_duration(self, user_id: int, subject: str, task_type: str, difficulty: str) -> str | None:
        from database.db import get_connection
        with get_connection() as conn:
            rows = conn.execute("""SELECT e.actual_duration FROM tasks t JOIN execution_records e ON e.task_id=t.id AND e.user_id=t.user_id WHERE t.user_id=? AND t.subject=? AND t.task_type=? AND t.difficulty=? AND e.actual_duration>0 ORDER BY t.task_date DESC LIMIT 10""", (user_id, subject, task_type, difficulty)).fetchall()
        if len(rows) < 3: return None
        avg = sum(r["actual_duration"] for r in rows) / len(rows)
        return f"历史类似任务平均实际用时：{avg:.0f}分钟；建议计划时长：{max(1, avg-3):.0f}–{avg+3:.0f}分钟"

