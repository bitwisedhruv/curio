import 'package:curio/theme/colors.dart';
import 'package:flutter/material.dart';

class SearchBarButton extends StatefulWidget {
  final IconData icon;
  final String text;
  const SearchBarButton({super.key, required this.icon, required this.text});

  @override
  State<SearchBarButton> createState() => _SearchBarButtonState();
}

class _SearchBarButtonState extends State<SearchBarButton> {
  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(6),
        color: Colors.transparent,
      ),
      child: Row(
        children: [
          Icon(
            widget.icon,
            color: AppColors.iconGrey,
            size: 20,
          ),
          const SizedBox(
            width: 8,
          ),
          Text(
            widget.text,
            style: const TextStyle(
              color: AppColors.textGrey,
            ),
          ),
        ],
      ),
    );
  }
}
