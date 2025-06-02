import GameImageQueue from "@/components/game-image-queue";
import DiscoveryQueueButton from "@/components/discovery-queue-button";
import { getGames } from "@/lib/games";
import { Separator } from "@/components/ui/separator";

export default async function Page() {
  const games = await getGames();

  return (
      <div className="container mx-auto px-4 py-4">
        
        <div className="grid gap-2 justify-center">
          <div className="grid rounded-xl bg-neutral-900/30 text-neutral-100 shadow-lg">
          <span className="text-4xl font-bald">YOUR DISCOVERY QUEUE</span>
          <span className="text-lg">
            Your recommendations are a mix of products that are similar to what
            you play on Steam.
            <br />
            Click below to get started, use the controls on each product page to
            like or dislike it as your recommendations. <br />
            Or jump to the next title in your queue.
          </span>
          </div>
          
          <Separator className="my-4"/>
          <div>
            <span className="text-lg font-bold">YOUR QUEUE</span>
            <GameImageQueue games={games} />
          </div>
          <DiscoveryQueueButton appid={games[0].appid}/>
          <div className="my-4">
            <Separator />

          </div>
          <div className="mb-8 p-6 rounded-xl bg-neutral-900/30 text-neutral-100 shadow-lg w-full mx-auto">
            <span className="text-3xl font-bold block mb-2">ABOUT THE RECOMMENDATION SYSTEM</span>
            <div className="mb-4">
              <span className="text-lg font-semibold">How does the recommendation system work?</span>
              <p className="text-base mt-1">
                The system analyzes your Steam games, taking into account your playtime and your preferences (likes/dislikes) in this app. It uses machine learning to find games similar to those you&apos;ve played, but also considers popularity, reviews, and developer diversity.
              </p>
            </div>
            <div className="mb-4">
              <span className="text-lg font-semibold">What factors influence recommendations?</span>
              <ul className="list-disc list-inside text-base mt-1 ml-2">
                <li>Your games and playtime</li>
                <li>Preferences: likes and dislikes</li>
                <li>Description, genres, tags, developer, and publisher of each game</li>
                <li>User reviews and game popularity on Steam</li>
                <li>Diversity — the system avoids recommending too many games from the same developer</li>
              </ul>
            </div>
            <div className="mb-4">
              <span className="text-lg font-semibold">How does the system decide what you&apos;ll like?</span>
              <p className="text-base mt-1">
                The system builds your profile based on the games you&apos;ve played and your preferences. It learns from this data and predicts which new games you might enjoy by comparing their features to your favorite games.
              </p>
            </div>
            <div className="mb-4">
              <span className="text-lg font-semibold">Why is it important to like or dislike games?</span>
              <p className="text-base mt-1">
                Your ratings help the system better understand your tastes. Liking a game boosts recommendations for similar games, while disliking reduces the chance of similar products appearing in your queue.
              </p>
            </div>
            <div>
              <span className="text-lg font-semibold">Are reviews and popularity considered?</span>
              <p className="text-base mt-1">
                Yes, the system takes into account the ratio of positive to negative reviews, as well as the overall popularity of a game, to recommend high-quality and interesting products.
              </p>
            </div>
          </div>
        </div>
      </div>
  );
}