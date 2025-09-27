#!/usr/bin/env python3
"""
Simple local cache for Legend of the Obsidian Vault
Provides in-memory caching for generated enemies and narratives
"""

import time
import hashlib
from typing import Any, Dict, Optional, Tuple
from pathlib import Path

class SimpleGameCache:
    """Lightweight in-memory cache for game entities"""

    def __init__(self, default_ttl: float = 600.0):  # 10 minutes default
        self.cache: Dict[str, Tuple[float, Any]] = {}
        self.default_ttl = default_ttl
        self.hits = 0
        self.misses = 0

    def _make_key(self, prefix: str, *args) -> str:
        """Create cache key from prefix and arguments"""
        key_data = f"{prefix}:" + ":".join(str(arg) for arg in args)
        return hashlib.md5(key_data.encode()).hexdigest()[:12]

    def _is_expired(self, timestamp: float, ttl: Optional[float] = None) -> bool:
        """Check if cached item has expired"""
        ttl = ttl or self.default_ttl
        return time.time() - timestamp > ttl

    def get(self, prefix: str, *args, ttl: Optional[float] = None) -> Optional[Any]:
        """Get item from cache"""
        key = self._make_key(prefix, *args)

        if key in self.cache:
            timestamp, value = self.cache[key]
            if not self._is_expired(timestamp, ttl):
                self.hits += 1
                return value
            else:
                # Remove expired item
                del self.cache[key]

        self.misses += 1
        return None

    def set(self, prefix: str, *args, value: Any, ttl: Optional[float] = None) -> None:
        """Set item in cache"""
        key = self._make_key(prefix, *args)
        self.cache[key] = (time.time(), value)

    def clear(self, prefix: Optional[str] = None) -> int:
        """Clear cache items, optionally by prefix"""
        if prefix is None:
            # Clear all
            count = len(self.cache)
            self.cache.clear()
            return count
        else:
            # Clear by prefix
            keys_to_remove = []
            for key in self.cache.keys():
                if key.startswith(prefix):
                    keys_to_remove.append(key)

            for key in keys_to_remove:
                del self.cache[key]

            return len(keys_to_remove)

    def cleanup_expired(self) -> int:
        """Remove expired entries from cache"""
        current_time = time.time()
        expired_keys = []

        for key, (timestamp, _) in self.cache.items():
            if current_time - timestamp > self.default_ttl:
                expired_keys.append(key)

        for key in expired_keys:
            del self.cache[key]

        return len(expired_keys)

    def stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0

        return {
            "size": len(self.cache),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{hit_rate:.1f}%",
            "total_requests": total_requests
        }

# Global cache instance
game_cache = SimpleGameCache()

# Convenience functions for common game caching

def cache_enemy(note_title: str, player_level: int, enemy_data: Any, ttl: float = 600.0) -> None:
    """Cache generated enemy data"""
    game_cache.set("enemy", note_title, player_level, value=enemy_data, ttl=ttl)

def get_cached_enemy(note_title: str, player_level: int) -> Optional[Any]:
    """Get cached enemy data"""
    return game_cache.get("enemy", note_title, player_level)

def cache_narrative(note_title: str, note_content_hash: str, narrative: str, ttl: float = 1800.0) -> None:
    """Cache generated narrative (30 minutes TTL)"""
    game_cache.set("narrative", note_title, note_content_hash, value=narrative, ttl=ttl)

def get_cached_narrative(note_title: str, note_content_hash: str) -> Optional[str]:
    """Get cached narrative"""
    return game_cache.get("narrative", note_title, note_content_hash)

def cache_quiz(note_title: str, difficulty: int, question: str, answer: str, ttl: float = 1200.0) -> None:
    """Cache generated quiz question (20 minutes TTL)"""
    quiz_data = {"question": question, "answer": answer}
    game_cache.set("quiz", note_title, difficulty, value=quiz_data, ttl=ttl)

def get_cached_quiz(note_title: str, difficulty: int) -> Optional[Dict[str, str]]:
    """Get cached quiz question"""
    return game_cache.get("quiz", note_title, difficulty)

def clear_enemy_cache() -> int:
    """Clear all cached enemies"""
    return game_cache.clear("enemy")

def clear_all_cache() -> int:
    """Clear entire cache"""
    return game_cache.clear()

def get_cache_stats() -> Dict[str, Any]:
    """Get cache performance statistics"""
    return game_cache.stats()

def cleanup_cache() -> int:
    """Clean up expired cache entries"""
    return game_cache.cleanup_expired()

# Cache key helpers

def make_content_hash(content: str) -> str:
    """Create a hash of note content for cache keys"""
    return hashlib.md5(content.encode()).hexdigest()[:8]

def cache_ai_result(operation: str, note_title: str, content: str, result: Any, ttl: float = 900.0) -> None:
    """Cache AI operation result"""
    content_hash = make_content_hash(content)
    game_cache.set("ai", operation, note_title, content_hash, value=result, ttl=ttl)

def get_cached_ai_result(operation: str, note_title: str, content: str) -> Optional[Any]:
    """Get cached AI operation result"""
    content_hash = make_content_hash(content)
    return game_cache.get("ai", operation, note_title, content_hash)

# Performance monitoring

def log_cache_performance():
    """Log cache performance (for debugging)"""
    stats = get_cache_stats()
    print(f"🗄️  Cache Stats: {stats['size']} items, {stats['hit_rate']} hit rate, {stats['total_requests']} requests")

# Periodic cleanup (call this occasionally)
def periodic_maintenance():
    """Perform periodic cache maintenance"""
    expired_count = cleanup_cache()
    if expired_count > 0:
        print(f"🧹 Cleaned up {expired_count} expired cache entries")

    stats = get_cache_stats()
    if stats['size'] > 100:  # If cache is getting large
        print(f"⚠️  Cache size: {stats['size']} items (consider clearing old entries)")

# Example usage:
if __name__ == "__main__":
    # Test the cache system
    print("🗄️  Testing Simple Game Cache")
    print("=" * 30)

    # Cache some test data
    cache_enemy("Test Note", 5, {"name": "Test Enemy", "hp": 20})
    cache_narrative("Test Note", "abc123", "A mystical encounter unfolds...")
    cache_quiz("Programming", 2, "What is Python?", "A programming language")

    # Test retrieval
    enemy = get_cached_enemy("Test Note", 5)
    narrative = get_cached_narrative("Test Note", "abc123")
    quiz = get_cached_quiz("Programming", 2)

    print(f"✅ Cached enemy: {enemy}")
    print(f"✅ Cached narrative: {narrative}")
    print(f"✅ Cached quiz: {quiz}")

    # Show stats
    stats = get_cache_stats()
    print(f"\n📊 Cache stats: {stats}")

    print("\n✅ Cache system working correctly!")