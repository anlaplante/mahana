BEGIN;
--
-- Alter field location on employee
--
ALTER TABLE `app_employee` DROP FOREIGN KEY `app_e_StockLocationID_7462a154_fk_stock_location_StockLocationID`;
ALTER TABLE `app_employee` MODIFY `StockLocationID` integer NULL;
ALTER TABLE `app_employee` ADD CONSTRAINT `app_e_StockLocationID_7462a154_fk_stock_location_StockLocationID` FOREIGN KEY (`StockLocationID`) REFERENCES `stock_location` (`StockLocationID`);

COMMIT;
