import OffersGrid from "../components/OffersGrid";
import { offersBySegment } from "../data/mockData";

function Offers() {
  return (
    <div className="space-y-6">
      <OffersGrid offers={offersBySegment} />
    </div>
  );
}

export default Offers;
