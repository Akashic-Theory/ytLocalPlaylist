#ifndef YTLP_SONGMETADATA_H
#define YTLP_SONGMETADATA_H

#include <cstdint>
#include <string>

struct SongMetaData {
	uint64_t id;

	bool setID(const std::string& token);
	[[nodiscard]] std::string getToken() const noexcept;
};


#endif //YTLP_SONGMETADATA_H
