import 'package:curio/theme/colors.dart';
import 'package:curio/widget/answer_block.dart';
import 'package:curio/widget/custom_side_bar.dart';
import 'package:curio/widget/source_block.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

class ChatPage extends StatelessWidget {
  final String query;
  const ChatPage({super.key, required this.query});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: [
          kIsWeb ? const CustomSideBar() : const SizedBox.shrink(),
          kIsWeb
              ? const SizedBox(
                  width: 100,
                )
              : const SizedBox.shrink(),
          Expanded(
            child: SingleChildScrollView(
              child: Padding(
                padding: const EdgeInsets.all(24.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      query,
                      style: const TextStyle(
                        fontSize: 40,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(
                      height: 24,
                    ),
                    const SourceBlocks(),
                    const SizedBox(
                      height: 24,
                    ),
                    const AnswerBlock(),
                  ],
                ),
              ),
            ),
          ),
          kIsWeb
              ? const Placeholder(
                  strokeWidth: 0,
                  color: AppColors.background,
                )
              : const SizedBox.shrink(),
        ],
      ),
    );
  }
}
