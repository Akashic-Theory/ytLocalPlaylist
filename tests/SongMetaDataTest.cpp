#include <catch2/catch_test_macros.hpp>
#include "../src/SongMetaData.h"

TEST_CASE("SongMetaData id conversions are valid", "[metadata][SongMetaData]") {
	SongMetaData dat{};
	dat.id = 0;
	SECTION("Happy Path") {
		std::string tokens[] = {
			"c61BuM8YzNg",
			"JwoqQuixiV0",
			"_VA6eSOO88M",
			"kQQB29kQnqw",
			"70ByjZkJX28",
			"C76yS0OtJNA",
			"Km_3HavZ6U0",
			"Nhs_hDyZpwk",
			"mC9MCTmbiXo",
			"G2w_luBdrsA"
		};
		SECTION("Token conversion is reversible") {
			for (const auto &token : tokens) {
				INFO("Failed with token - " << token);
				REQUIRE(dat.setID(token));
				REQUIRE(dat.getToken() == token);
			}
		}
	}
	SECTION("setID invalid token returns false") {
		SECTION("Token too short") {
			REQUIRE_FALSE(dat.setID("TOOSHORT"));
		}

		SECTION("Token too long") {
			REQUIRE_FALSE(dat.setID("TOKENMUCHTOOLONG"));
		}

		SECTION("Token contains invalid characters") {
			REQUIRE_FALSE(dat.setID("~ !@#$%^&*+"));
		}

		SECTION("Final character contains incorrect subset") {
			for (char c: "BCDFGHJKLNOPRSTVWXZabdefhijlmnpqrtuvxyz1235679-_") {
				std::string base = "__________";
				INFO("FAILED with character - " << c);
				CHECK_FALSE(dat.setID(base + c));
			}
		}
	}
}