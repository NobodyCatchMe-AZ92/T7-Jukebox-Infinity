// Memory-safe copy used by the main-menu code (mainmenu.hpp). The dev menu tracer that lived here (menu recon,
// 2026-11-10) was removed for the release (docs/TECHNICAL.md describes what it found).
#pragma once
#include <cstdint>
#include <cstring>

#include "common.hpp"

namespace jb::mtrace {

// copy n bytes from a game address; false if the memory is not readable
inline bool safe_copy(void *dst, uintptr_t src, size_t n)
{
	__try
	{
		memcpy(dst, reinterpret_cast<const void *>(src), n);
		return true;
	}
	__except (EXCEPTION_EXECUTE_HANDLER)
	{
		return false;
	}
}

} // namespace jb::mtrace
