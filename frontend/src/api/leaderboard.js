import client from './client'

export const leaderboardApi = {
  get: (dimension) => client.get('/leaderboard', { params: dimension ? { dimension } : {} }),
}
