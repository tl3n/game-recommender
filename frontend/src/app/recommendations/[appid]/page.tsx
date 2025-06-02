import GameNavigation from "@/components/game-navigation";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel";
import { getGames } from "@/lib/games";
import Image from "next/image";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";

interface PageProps {
  params: Promise<{ appid: string }>;
}

export default async function Page({ params }: PageProps) {
  const { appid } = await params;
  const games = await getGames();
  const game = games.find((g) => g.appid == appid);

  const currentIndex = games.findIndex((g) => g.appid == appid);
  const prevGame = currentIndex !== 0 ? games[currentIndex - 1] : "";
  const nextGame =
    currentIndex !== games.length - 1 ? games[currentIndex + 1] : "";

  return (
      <div className="container mx-auto px-4 py-4">
        <div className="flex flex-col gap-4">
          <div className="flex flex-col lg:flex-row gap-8">
            <div className="w-full lg:w-5/6">
              <Carousel className="relative">
                <CarouselContent>
                  {game?.screenshots.map((image: string, index: number) => (
                    <CarouselItem key={index}>
                      <div className="relative aspect-video">
                        <Image
                          src={image}
                          alt={`Image ${index + 1}`}
                          fill
                          className="rounded-xl object-contain"
                          priority={index === 0}
                        />
                      </div>
                    </CarouselItem>
                  ))}
                </CarouselContent>
                <div className="absolute left-15 top-1/2 -translate-y-1/2">
                  <CarouselPrevious className="h-8 w-8" />
                </div>
                <div className="absolute right-15 top-1/2 -translate-y-1/2">
                  <CarouselNext className="h-8 w-8" />
                </div>
              </Carousel>
            </div>

            <div className="w-full lg:w-1/3">
              <div className="bg-neutral-900/30 px-4 rounded-xl h-full">
                <div className="h-full overflow-y-auto space-y-4">
                  <div className="relative w-full aspect-[2/1]">
                    <Image
                      src={game?.headerImage!}
                      alt={`${game?.name} header image`}
                      fill
                      className="rounded-xl object-cover"
                    />
                  </div>
                  <div>
                    <span className="text-2xl font-bold">{game?.name}</span>
                  </div>

                  <div className="space-y-2">
                    <p className="text-sm">{game?.shortDescription}</p>
                    <Separator />
                    <div className="mt-4 space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-xs text-neutral-300">
                          RELEASE DATE:
                        </span>
                        <p>{game?.releaseDate}</p>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-xs text-neutral-300">
                          DEVELOPER:
                        </span>
                        <p>{game?.developer}</p>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-xs text-neutral-300">
                          PUBLISHER:
                        </span>
                        <p>{game?.publisher}</p>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-xs text-neutral-300">
                          RECOMMENDATION SCORE:
                        </span>
                        <p>{game?.recommendationScore?.toFixed(1)}%</p>
                      </div>
                      <Separator />
                      <span className="text-xs text-neutral-300">
                        Popular user-defined tags for this product:
                      </span>
                      <div className="flex items-center justify-center">
                        {game?.tags && game.tags.length > 0 && (
                          <div className="flex flex-wrap gap-2 mt-2">
                            {game.tags
                              .slice(0, 5)
                              .map((tag: string, idx: number) => (
                                <Badge key={idx} variant="secondary">
                                  {tag}
                                </Badge>
                              ))}
                          </div>
                        )}
                      </div>
                      <div className="mt-4"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="bg-neutral-900/30 p-2 rounded-xl my-4">
          <GameNavigation
            game={game!}
            prevGameId={prevGame ? prevGame.appid : undefined}
            nextGameId={nextGame ? nextGame.appid : undefined}
          />
        </div>
        <Separator />
        <div className="bg-neutral-900/30 p-2 rounded-xl my-4 ">
          <p className="text-md text-neutral-300">
            {game?.detailedDescription}
          </p>
        </div>
      </div>
  );
}
