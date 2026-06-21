USER_PROFILE_QUERY = """
query userPublicProfile($username: String!) {
    matchedUser(username: $username) {
        username
        profile {
            ranking
            userAvatar
            realName
            aboutMe
            school
            websites
            countryName
            reputation
        }
        submitStats {
            acSubmissionNum {
                difficulty
                count
            }
        }
    }
}
"""