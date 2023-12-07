from typing import Dict

query_string = """
query GetUserMatches($steamId: Long!, $numMatches: Int!) {
    player(steamAccountId:$steamId)
    {
        matches(request: {
            isParsed: true,
            take: $numMatches,
            orderBy:DESC,
            rankIds:[80]

    }) {
        id
        endDateTime
        didRequestDownload
        durationSeconds
        ...MatchBuildsMatchTypeFragment
        ...MatchGraphs
        ...MatchLog
        ...MatchPerformance
        ...MatchScoreboard
        ...HeroGuideMatch
        players {
          ...HeroGuideMatchPlayer
          ...HeroGuideMatchPlayerOther
          __typename
        }
        __typename
      }
    }
}

fragment HeroGuideMatch on MatchType {
  ...HeroGuideTimelineMatch
  ...HeroGuidePickBan
  __typename
}

fragment HeroGuideMatchPlayer on MatchPlayerType {
  ...HeroGuideTimelineMatchPlayer
  ...HeroGuideAbilityBuildMatchPlayer
  ...HeroGuidePostGameStatsMatchPlayer
  ...HeroGuidePickBanPlayer
  __typename
}

fragment HeroGuideMatchPlayerOther on MatchPlayerType {
  ...HeroGuideTimelineMatchPlayerOther
  ...HeroGuidePostGameStatsMatchPlayerOther
  __typename
}

fragment HeroGuideTimelineMatch on MatchType {
  durationSeconds
  towerDeaths {
    npcId
    time
    isRadiant
    __typename
  }
  gameVersionId
  __typename
}

fragment HeroGuideTimelineMatchPlayerOther on MatchPlayerType {
  lane
  position
  heroId
  stats {
    networthPerMinute
    level
    wards {
      positionX
      positionY
      time
      type
      __typename
    }
    __typename
  }
  __typename
}

fragment HeroGuideTimelineMatchPlayer on MatchPlayerType {
  lane
  position
  stats {
    itemPurchases {
      time
      itemId
      __typename
    }
    inventoryReport {
      backPack0 {
        ...inventoryReportItem
        __typename
      }
      backPack1 {
        ...inventoryReportItem
        __typename
      }
      backPack2 {
        ...inventoryReportItem
        __typename
      }
      item0 {
        ...inventoryReportItem
        __typename
      }
      item1 {
        ...inventoryReportItem
        __typename
      }
      item2 {
        ...inventoryReportItem
        __typename
      }
      item3 {
        ...inventoryReportItem
        __typename
      }
      item4 {
        ...inventoryReportItem
        __typename
      }
      item5 {
        ...inventoryReportItem
        __typename
      }
      neutral0 {
        ...inventoryReportItem
        __typename
      }
      __typename
    }
    spiritBearInventoryReport {
      backPack0Id
      backPack1Id
      backPack2Id
      item0Id
      item1Id
      item2Id
      item3Id
      item4Id
      item5Id
      neutral0Id
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
    goldPerMinute
    experiencePerMinute
    lastHitsPerMinute
    deniesPerMinute
    level
    matchPlayerBuffEvent {
      abilityId
      itemId
      time
      stackCount
      __typename
    }
    __typename
  }
  additionalUnit {
    item0Id
    item1Id
    item2Id
    item3Id
    item4Id
    item5Id
    neutral0Id
    __typename
  }
  __typename
}

fragment inventoryReportItem on MatchPlayerInventoryObjectType {
  itemId
  charges
  __typename
}

fragment HeroGuideAbilityBuildMatchPlayer on MatchPlayerType {
  item0Id
  item1Id
  item2Id
  item3Id
  item4Id
  item5Id
  stats {
    itemPurchases {
      itemId
      __typename
    }
    __typename
  }
  abilities {
    abilityId
    level
    time
    __typename
  }
  __typename
}

fragment HeroGuidePostGameStatsMatchPlayerOther on MatchPlayerType {
  isRadiant
  kills
  __typename
}

fragment HeroGuidePostGameStatsMatchPlayer on MatchPlayerType {
  isRadiant
  kills
  deaths
  assists
  level
  networth
  imp
  goldPerMinute
  experiencePerMinute
  numLastHits
  numDenies
  heroDamage
  towerDamage
  heroAverage {
    time
    kills
    deaths
    assists
    networth
    xp
    cs
    dn
    heroDamage
    towerDamage
    __typename
  }
  __typename
}

fragment HeroGuidePickBan on MatchType {
  pickBans {
    bannedHeroId
    isPick
    playerIndex
    isRadiant
    order
    heroId
    __typename
  }
  __typename
}

fragment HeroGuidePickBanPlayer on MatchPlayerType {
  playerSlot
  __typename
}

fragment MatchBuildsMatchTypeFragment on MatchType {
  durationSeconds
  endDateTime
  gameMode
  didRadiantWin
  statsDateTime
  radiantKills
  direKills
  players {
    isRadiant
    position
    heroId
    level
    neutral0Id
    steamAccount {
      id
      ...PlayerNameColSteamAccountTypeFragment
      __typename
    }
    stats {
      inventoryReport {
        backPack0 {
          ...inventoryReportItem
          __typename
        }
        backPack1 {
          ...inventoryReportItem
          __typename
        }
        backPack2 {
          ...inventoryReportItem
          __typename
        }
        item0 {
          ...inventoryReportItem
          __typename
        }
        item1 {
          ...inventoryReportItem
          __typename
        }
        item2 {
          ...inventoryReportItem
          __typename
        }
        item3 {
          ...inventoryReportItem
          __typename
        }
        item4 {
          ...inventoryReportItem
          __typename
        }
        item5 {
          ...inventoryReportItem
          __typename
        }
        neutral0 {
          ...inventoryReportItem
          __typename
        }
        __typename
      }
      itemPurchases {
        time
        itemId
        __typename
      }
      level
      __typename
    }
    abilities {
      abilityId
      time
      level
      __typename
    }
    __typename
  }
  __typename
}

fragment PlayerNameColSteamAccountTypeFragment on SteamAccountType {
  id
  name
  proSteamAccount {
    name
    __typename
  }
  isAnonymous
  isStratzPublic
  smurfFlag
  __typename
}

fragment MatchGraphs on MatchType {
  durationSeconds
  winRates
  radiantNetworthLeads
  players {
    stats {
      level
      lastHitsPerMinute
      networthPerMinute
      actionsPerMinute
      heroDamagePerMinute
      healPerMinute
      __typename
    }
    __typename
  }
  __typename
}

fragment MatchLog on MatchType {
  id
  endDateTime
  statsDateTime
  towerDeaths {
    attacker
    npcId
    time
    isRadiant
    __typename
  }
  chatEvents {
    isRadiant
    time
    value
    fromHeroId
    type
    pausedTick
    __typename
  }
  players {
    isRadiant
    heroId
    position
    steamAccount {
      id
      isAnonymous
      isStratzPublic
      name
      smurfFlag
      proSteamAccount {
        name
        __typename
      }
      __typename
    }
    stats {
      runes {
        time
        rune
        action
        __typename
      }
      allTalks {
        time
        message
        pausedTick
        __typename
      }
      chatWheels {
        time
        chatWheelId
        pausedTick: pauseTick
        __typename
      }
      killEvents {
        time
        target
        __typename
      }
      deathEvents {
        time
        attacker
        target
        __typename
      }
      __typename
    }
    __typename
  }
  __typename
}

fragment MatchPerformance on MatchType {
  ...MatchPerformanceDistribution
  ...MatchPerformanceSimulation
  __typename
}

fragment MatchPerformanceDistribution on MatchType {
  players {
    award
    heroId
    imp
    stats {
      impPerMinute
      __typename
    }
    __typename
  }
  __typename
}

fragment MatchPerformanceSimulation on MatchType {
  ...MatchPerformanceSimulationHeroSection
  ...MatchPerformanceSimulationStatDataRowList
  __typename
}

fragment MatchPerformanceSimulationHeroSection on MatchType {
  rank
  players {
    heroId
    position
    steamAccount {
      id
      name
      isAnonymous
      isStratzPublic
      smurfFlag
      seasonRank
      proSteamAccount {
        name
        __typename
      }
      __typename
    }
    __typename
  }
  __typename
}

fragment MatchPerformanceSimulationStatDataRowList on MatchType {
  players {
    heroId
    __typename
  }
  __typename
}

fragment MatchScoreboard on MatchType {
  players {
    position
    heroId
    level
    partyId
    imp
    kills
    deaths
    assists
    networth
    isRadiant
    award
    backpack0Id
    backpack1Id
    backpack2Id
    item0Id
    item1Id
    item2Id
    item3Id
    item4Id
    item5Id
    neutral0Id
    numLastHits
    numDenies
    heroDamage
    towerDamage
    heroHealing
    steamAccount {
      ...PlayerNameColSteamAccountTypeFragment
      __typename
    }
    additionalUnit {
      item0Id
      item1Id
      item2Id
      item3Id
      item4Id
      item5Id
      neutral0Id
      __typename
    }
    stats {
      impPerMinute
      networthPerMinute
      goldPerMinute
      campStack
      heroDamageReceivedPerMinute
      experiencePerMinute
      lastHitsPerMinute
      deniesPerMinute
      heroDamagePerMinute
      towerDamagePerMinute
      healPerMinute
      level
      killEvents {
        time
        target
        __typename
      }
      deathEvents {
        time
        timeDead
        goldLost
        __typename
      }
      assistEvents {
        time
        __typename
      }
      runes {
        time
        rune
        action
        __typename
      }
      itemPurchases {
        time
        itemId
        __typename
      }
      matchPlayerBuffEvent {
        time
        abilityId
        itemId
        stackCount
        __typename
      }
      inventoryReport {
        backPack0 {
          ...inventoryReportItem
          __typename
        }
        backPack1 {
          ...inventoryReportItem
          __typename
        }
        backPack2 {
          ...inventoryReportItem
          __typename
        }
        item0 {
          ...inventoryReportItem
          __typename
        }
        item1 {
          ...inventoryReportItem
          __typename
        }
        item2 {
          ...inventoryReportItem
          __typename
        }
        item3 {
          ...inventoryReportItem
          __typename
        }
        item4 {
          ...inventoryReportItem
          __typename
        }
        item5 {
          ...inventoryReportItem
          __typename
        }
        neutral0 {
          ...inventoryReportItem
          __typename
        }
        __typename
      }
      spiritBearInventoryReport {
        item0Id
        item1Id
        item2Id
        item3Id
        item4Id
        item5Id
        neutral0Id
        __typename
      }
      __typename
    }
    __typename
  }
  pickBans {
    heroId
    isCaptain
    __typename
  }
  ...MatchFactionHeaderMatchTypeFragment
  __typename
}

fragment MatchFactionHeaderMatchTypeFragment on MatchType {
  didRadiantWin
  radiantTeam {
    ...MatchFactionHeaderTeamTypeFragment
    __typename
  }
  direTeam {
    ...MatchFactionHeaderTeamTypeFragment
    __typename
  }
  __typename
}

fragment MatchFactionHeaderTeamTypeFragment on TeamType {
  id
  name
  __typename
}
"""


def build_query(steam_id: int, num_matches: int = 10) -> Dict:
    """
    Build the GraphQL query to request old matches of a player
    :param num_matches: the number of matches to request
    """
    query = {
        "operationName": "GetUserMatches",
        "variables": {"steamId": steam_id, "numMatches": num_matches},
        "query": query_string,
    }

    return query
