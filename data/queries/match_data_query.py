from typing import Dict

query_string = """
    query LiveMatch($matchId: Long!) {
        live {
            match(id: $matchId) {
            matchId
            gameMode
            gameTime
            isParsing
            leagueId
            playbackData {
                buildingEvents {
                npcId
                isAlive
                __typename
                }
                __typename
            }
            players {
                steamAccountId
                heroId
                __typename
            }
            ...LiveMinimapMatchLiveTypeFragment
            ...LiveHeaderMatchLiveTypeFragment
            ...LiveStatsMatchLiveTypeFragment
            ...LiveProviderMatchLiveTypeFragment
            ...LiveDraftMatchLiveTypeFragment
            ...LiveDescriptionMatchLiveTypeFragment
            ...LiveSummaryRowMatchLiveTypeFragment
            ...LiveLogMatchLiveTypeFragment
            ...GetGameStateMatchLiveTypeFragment
            ...LiveStreamsMatchLiveTypeFragment
            ...LiveInsightsPreDraftMatchLiveTypeFragment
            ...LiveInsightsPostDraftMatchLiveTypeFragment
            __typename
            }
            __typename
        }
        match(id: $matchId) {
            id
            __typename
        }
        }

        fragment LiveMinimapMatchLiveTypeFragment on MatchLiveType {
        players {
            heroId
            isRadiant
            playbackData {
            positionEvents {
                x
                y
                time
                __typename
            }
            __typename
            }
            ...LiveMinimapHeroHoverCardMatchLivePlayerTypeFragment
            __typename
        }
        playbackData {
            buildingEvents {
            npcId
            isAlive
            time
            positionX
            __typename
            }
            __typename
        }
        gameTime
        ...LiveScoreAndTimeMatchLiveTypeFragment
        __typename
        }

        fragment LiveMinimapHeroHoverCardMatchLivePlayerTypeFragment on MatchLivePlayerType {
        heroId
        level
        steamAccount {
            ...SteamAccountHoverCardSteamAccountTypeFragment
            __typename
        }
        __typename
        }

        fragment SteamAccountHoverCardSteamAccountTypeFragment on SteamAccountType {
        id
        name
        avatar
        isAnonymous
        isStratzPublic
        smurfFlag
        proSteamAccount {
            name
            team {
            id
            tag
            __typename
            }
            __typename
        }
        __typename
        }

        fragment LiveScoreAndTimeMatchLiveTypeFragment on MatchLiveType {
        gameTime
        radiantScore
        direScore
        radiantTeam {
            ...LiveScoreAndTimeTeamTypeFragment
            __typename
        }
        direTeam {
            ...LiveScoreAndTimeTeamTypeFragment
            __typename
        }
        playbackData {
            radiantScore {
            ...LiveScoreAndTimeMatchLiveTeamScoreDetailTypeFragment
            __typename
            }
            direScore {
            ...LiveScoreAndTimeMatchLiveTeamScoreDetailTypeFragment
            __typename
            }
            __typename
        }
        __typename
        }

        fragment LiveScoreAndTimeTeamTypeFragment on TeamType {
        id
        name
        __typename
        }

        fragment LiveScoreAndTimeMatchLiveTeamScoreDetailTypeFragment on MatchLiveTeamScoreDetailType {
        time
        score
        __typename
        }

        fragment LiveHeaderMatchLiveTypeFragment on MatchLiveType {
        radiantTeam {
            ...LiveHeaderTeamTypeFragment
            __typename
        }
        direTeam {
            ...LiveHeaderTeamTypeFragment
            __typename
        }
        ...LiveHeaderAvatarMatchLiveTypeFragment
        ...GetDidRadiantWinMatchLiveTypeFragment
        __typename
        }

        fragment LiveHeaderTeamTypeFragment on TeamType {
        id
        name
        __typename
        }

        fragment LiveHeaderAvatarMatchLiveTypeFragment on MatchLiveType {
        players {
            heroId
            __typename
        }
        playbackData {
            pickBans {
            heroId
            isPick
            isRadiant
            __typename
            }
            __typename
        }
        __typename
        }

        fragment GetDidRadiantWinMatchLiveTypeFragment on MatchLiveType {
        playbackData {
            buildingEvents {
            npcId
            isAlive
            __typename
            }
            __typename
        }
        __typename
        }

        fragment LiveStatsMatchLiveTypeFragment on MatchLiveType {
        gameTime
        players {
            isRadiant
            lastHits: numLastHits
            denies: numDenies
            kills: numKills
            deaths: numDeaths
            assists: numAssists
            level
            experiencePerMinute
            gold
            networth
            goldPerMinute
            impPerMinute {
            time
            imp
            __typename
            }
            ...LiveStatsBaseRowMatchLivePlayerTypeFragment
            ...LiveStatsInventoryMatchLivePlayerTypeFragment
            __typename
        }
        ...LiveStatsPlayerHeroGraphMatchLiveTypeFragment
        ...LiveStatsFactionsPlayersGraphMatchLiveTypeFragment
        __typename
        }

        fragment LiveStatsBaseRowMatchLivePlayerTypeFragment on MatchLivePlayerType {
        playerSlot
        steamAccount {
            id
            avatar
            name
            proSteamAccount {
            name
            __typename
            }
            __typename
        }
        heroId
        respawnTimer
        position
        __typename
        }

        fragment LiveStatsPlayerHeroGraphMatchLiveTypeFragment on MatchLiveType {
        gameTime
        players {
            heroId
            isRadiant
            playerSlot
            playbackData {
            goldEvents {
                time
                gold
                networth
                __typename
            }
            levelEvents {
                time
                level
                __typename
            }
            killEvents {
                time
                __typename
            }
            deathEvents {
                time
                __typename
            }
            assistEvents {
                time
                __typename
            }
            lastHitEvents: csEvents {
                time
                __typename
            }
            experienceEvents {
                time
                experiencePerMinute: expPerMinute
                __typename
            }
            __typename
            }
            __typename
        }
        __typename
        }

        fragment LiveStatsFactionsPlayersGraphMatchLiveTypeFragment on MatchLiveType {
        gameTime
        radiantTeam {
            ...LiveStatsFactionsPlayersGraphTeamTypeFragment
            __typename
        }
        direTeam {
            ...LiveStatsFactionsPlayersGraphTeamTypeFragment
            __typename
        }
        __typename
        }

        fragment LiveStatsFactionsPlayersGraphTeamTypeFragment on TeamType {
        id
        name
        __typename
        }

        fragment LiveStatsInventoryMatchLivePlayerTypeFragment on MatchLivePlayerType {
        playbackData {
            inventoryEvents {
            time
            backpack0Id: backpackId0
            backpack1Id: backpackId1
            backpack2Id: backpackId2
            item0Id: itemId0
            item1Id: itemId1
            item2Id: itemId2
            item3Id: itemId3
            item4Id: itemId4
            item5Id: itemId5
            __typename
            }
            __typename
        }
        __typename
        }

        fragment LiveProviderMatchLiveTypeFragment on MatchLiveType {
        gameTime
        players {
            heroId
            playbackData {
            goldEvents {
                time
                __typename
            }
            __typename
            }
            __typename
        }
        __typename
        }

        fragment LiveDraftMatchLiveTypeFragment on MatchLiveType {
        playbackData {
            pickBans {
            heroId
            bannedHeroId
            isPick
            isRadiant
            letter
            positionValues
            __typename
            }
            __typename
        }
        gameMode
        players {
            heroId
            position
            __typename
        }
        ...LiveDraftGraphMatchLiveTypeFragment
        __typename
        }

        fragment LiveDraftGraphMatchLiveTypeFragment on MatchLiveType {
        winRateValues
        durationValues
        radiantTeam {
            ...LiveDraftGraphTeamTypeFragment
            __typename
        }
        direTeam {
            ...LiveDraftGraphTeamTypeFragment
            __typename
        }
        __typename
        }

        fragment LiveDraftGraphTeamTypeFragment on TeamType {
        id
        name
        __typename
        }

        fragment LiveDescriptionMatchLiveTypeFragment on MatchLiveType {
        gameTime
        modifiedDateTime
        createdDateTime
        __typename
        }

        fragment LiveSummaryRowMatchLiveTypeFragment on MatchLiveType {
        matchId
        gameMode
        lobbyType
        averageRank
        delay
        league {
            id
            displayName
            __typename
        }
        __typename
        }

        fragment LiveLogMatchLiveTypeFragment on MatchLiveType {
        playbackData {
            buildingEvents {
            time
            npcId
            isAlive
            __typename
            }
            __typename
        }
        players {
            playbackData {
            inventoryEvents {
                time
                backpack0Id: backpackId0
                backpack1Id: backpackId1
                backpack2Id: backpackId2
                item0Id: itemId0
                item1Id: itemId1
                item2Id: itemId2
                item3Id: itemId3
                item4Id: itemId4
                item5Id: itemId5
                __typename
            }
            killEvents {
                time
                __typename
            }
            deathEvents {
                time
                __typename
            }
            __typename
            }
            heroId
            isRadiant
            __typename
        }
        gameTime
        ...LiveNetWorthMatchLiveTypeFragment
        __typename
        }

        fragment LiveNetWorthMatchLiveTypeFragment on MatchLiveType {
        radiantTeam {
            ...LiveNetWorthTeamTypeFragment
            __typename
        }
        direTeam {
            ...LiveNetWorthTeamTypeFragment
            __typename
        }
        players {
            playbackData {
            goldEvents {
                time
                networth
                __typename
            }
            __typename
            }
            isRadiant
            __typename
        }
        __typename
        }

        fragment LiveNetWorthTeamTypeFragment on TeamType {
        id
        name
        __typename
        }

        fragment GetGameStateMatchLiveTypeFragment on MatchLiveType {
        playbackData {
            buildingEvents {
            npcId
            isAlive
            __typename
            }
            __typename
        }
        isParsing
        players {
            heroId
            __typename
        }
        gameTime
        __typename
        }

        fragment LiveStreamsMatchLiveTypeFragment on MatchLiveType {
        radiantTeamId
        direTeamId
        gameTime
        league {
            streams {
            id
            broadcastProvider
            name
            streamUrl
            __typename
            }
            nodeGroups {
            nodes {
                teamOneId
                teamTwoId
                streamIds
                scheduledTime
                __typename
            }
            __typename
            }
            __typename
        }
        __typename
        }

        fragment LiveInsightsPreDraftMatchLiveTypeFragment on MatchLiveType {
        radiantTeam {
            ...LiveInsightsPreDraftTeamTypeFragment
            __typename
        }
        direTeam {
            ...LiveInsightsPreDraftTeamTypeFragment
            __typename
        }
        insight {
            teamOneVsWinCount
            teamTwoVsWinCount
            teamOneLeagueWinCount
            teamOneLeagueMatchCount
            teamTwoLeagueWinCount
            teamTwoLeagueMatchCount
            lastSeries {
            teamOneId
            teamTwoId
            teamOneWinCount
            teamTwoWinCount
            matches {
                id
                radiantTeamId
                direTeamId
                players {
                steamAccount {
                    ...SteamAccountHoverCardSteamAccountTypeFragment
                    __typename
                }
                __typename
                }
                __typename
            }
            __typename
            }
            __typename
        }
        players {
            steamAccount {
            ...SteamAccountHoverCardSteamAccountTypeFragment
            __typename
            }
            __typename
        }
        __typename
        }

        fragment LiveInsightsPreDraftTeamTypeFragment on TeamType {
        id
        name
        __typename
        }

        fragment LiveInsightsPostDraftMatchLiveTypeFragment on MatchLiveType {
        liveWinRateValues {
            time
            winRate
            __typename
        }
        gameTime
        winRateValues
        radiantTeam {
            ...LiveInsightsPostDraftTeamTypeFragment
            __typename
        }
        direTeam {
            ...LiveInsightsPostDraftTeamTypeFragment
            __typename
        }
        __typename
        }

        fragment LiveInsightsPostDraftTeamTypeFragment on TeamType {
        id
        name
        __typename
        }
"""


def build_query(match_id: int) -> Dict:
    """
    Build the GraphQL query to request match data
    :param num_matches: the number of matches to request
    """
    query = {
        "operationName": "LiveMatch",
        "variables": {
            "matchId": match_id,
        },
        "query": query_string,
    }

    return query
