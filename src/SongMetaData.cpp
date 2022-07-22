#include "SongMetaData.h"

namespace {
	const char tokenTable[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";
	inline uint8_t idTable(char token) {
		switch (token) {
			case 'A': case 'B': case 'C': case 'D': case 'E':
			case 'F': case 'G': case 'H': case 'I': case 'J':
			case 'K': case 'L': case 'M': case 'N': case 'O':
			case 'P': case 'Q': case 'R': case 'S': case 'T':
			case 'U': case 'V': case 'W': case 'X': case 'Y':
			case 'Z':
				return token - 'A';
			case 'a': case 'b': case 'c': case 'd': case 'e':
			case 'f': case 'g': case 'h': case 'i': case 'j':
			case 'k': case 'l': case 'm': case 'n': case 'o':
			case 'p': case 'q': case 'r': case 's': case 't':
			case 'u': case 'v': case 'w': case 'x': case 'y':
			case 'z':
				return token - 'a' + 26;
			case '0': case '1': case '2': case '3': case '4':
			case '5': case '6': case '7': case '8': case '9':
				return token - '0' + 52;
			case '-':
				return 62;
			case '_':
				return 63;
			default:
				return 0b10000000;
		}
	}
}

bool SongMetaData::setID(const std::string& token) {
	if (token.length() != 11) {
		return false;
	}
	uint64_t tmp_id = 0;
	uint8_t encode;
	for (int i = 0; i < 10; ++i) {
		encode = idTable(token[i]);
		if (encode & 0b11000000) {
			// We only encode 6 bits. Error if upper two bits are somehow set
			return false;
		}
		tmp_id += (uint64_t) encode << (6 * (10 - i) - 2);
	}
	encode = idTable(token[10]);
	if (encode & 0b11000011) {
		return false;
	}
	tmp_id |= encode >> 2;
	id = tmp_id;
	return true;
}

std::string SongMetaData::getToken() const noexcept {
	std::string token;
	for (int i = 10; i > 0; --i) {
		token += tokenTable[(id >> (i*6 - 2)) & 0b111111];
	}
	token += tokenTable[(id << 2) & 0b111100];
	return token;
}
